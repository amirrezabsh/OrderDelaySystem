from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.db.models import Count, Sum
from .models import Order, Trip, DelayReport, Vendor
from redis_utils import RedisQueue
from datetime import datetime, timedelta
from .serializers import VendorSerializer
from rest_framework.response import Response

# Get the singleton instance of DelaysQueue
delays_queue = RedisQueue()

def report_delay(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'Order not found'}, status=404)
    
    # Check if there's a related trip with the order
    if Trip.objects.filter(status__in=['VENDOR_AT', 'ASSIGNED', 'PICKED'],order=order).exists():

        # Call the external API to get a new delivery estimate
        response = requests.get('https://run.mocky.io/v3/122c2796-5df4-461c-ab75-87c1192b17f7')
        if response.status_code == 200:
            new_estimated_delivery = response.json().get('data').get('eta')

            # Update the order with the new estimated delivery time
            order.time_delivery = new_estimated_delivery
            order.save()


            report = DelayReport(order=order)
            report.save()

            return JsonResponse({'message': 'Order updated with new estimated time and the report has been submitted', 'new_estimated_time':new_estimated_delivery, 'report_id':report.id}, status=201)
        else:
            return JsonResponse({'message': 'Failed to get new estimated time'}, status=500)
        


    else:
        report = DelayReport(order=order)
        report.save()

        delays_queue.enqueue('delays', report.id)

        return JsonResponse({'message': 'Order put in delay queue'})

def weekly_vendors_by_delay(request):
    # Calculate the start and end date for the past week
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)

    # Get vendors with their total delays in the past week
    vendors = Vendor.objects.annotate(
        total_delays=Sum('order__trip__delayreport__order__time_stamp__range', 
                            filter=models.Q(order__trip__delayreport__time_stamp__range=(start_date, end_date)),
                            distinct=True)
        ).order_by('-total_delays')
    
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)