from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.db.models import OuterRef, Subquery, Count, Sum, Q, ExpressionWrapper, DurationField, F, Max
from .models import Order, Trip, DelayReport, Vendor
from redis_utils import RedisQueue
from datetime import datetime, timedelta
from .serializers import VendorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone

# Get the singleton instance of DelaysQueue
delays_queue = RedisQueue()
queue_name = 'delays'

@api_view(['GET'])
def report_delay(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'Order not found'}, status=404)
    
    current_time = timezone.now()
    if order.delivery_time + order.time_stamp > current_time:
        return JsonResponse({'message': 'Cannot report delay before the estimated delivery time has passed','time':timezone.now()}, status=400)
    

    delayed_order_ids = DelayReport.objects.filter(order=order, agent=None, is_checked=False).values_list('id', flat=True)
    if delayed_order_ids:
        exists_in_queue = delays_queue.exists(queue_name, *delayed_order_ids)
        if exists_in_queue:
            return JsonResponse({'message': 'The order is already in the waiting queue'}, status=400)


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

        # Enqueue the delay report to the delays_queue
        delays_queue.enqueue(queue_name, report.id)

        return JsonResponse({'message': 'Order put in delay queue'})
    
@api_view(['GET'])
def weekly_vendors(request):
    # Calculate the start and end date for the past week
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    # Subquery to calculate the maximum delay duration for each order of a vendor in the past week
    total_delays_subquery = DelayReport.objects.filter(
        order__time_stamp__range=(start_date, end_date),
        order__delayreport__isnull=False
    ).annotate(
        total_delay=ExpressionWrapper(
            F('time_stamp') - (F('order__time_stamp') + F('order__delivery_time')),
            output_field=DurationField()
        )
    ).values('order__vendor').annotate(max_total_delay=Max('total_delay')).values('max_total_delay')

    # Get vendors with their maximum delays in the past week
    vendors = Vendor.objects.filter(
        order__delayreport__isnull=False
    ).annotate(
        max_total_delay=Subquery(total_delays_subquery)
    ).order_by('-max_total_delay')
    
    serializer = VendorSerializer(vendors, many=True)

    return JsonResponse({'message': 'Successful', 'data': serializer.data}, status=200)