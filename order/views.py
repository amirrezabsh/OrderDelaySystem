from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.db.models import OuterRef, Subquery, Count, Sum, DecimalField, Q, ExpressionWrapper, IntegerField, DurationField, F, Max, FloatField, DateTimeField
from .models import Order, Trip, DelayReport
from redis_utils import RedisQueue
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from django.db.models.functions import Cast, Coalesce
# Get the singleton instance of DelaysQueue
delays_queue = RedisQueue()
queue_name = 'delays'
# Create your views here.


@api_view(['GET'])
def report_delay(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'Order not found'}, status=404)
    
    current_time = timezone.now()
    if timedelta(minutes=(order.delivery_time + order.eta)) + order.time_stamp > current_time:
        return JsonResponse({'message': 'Cannot report delay before the estimated delivery time has passed','time':timezone.now()}, status=400)

    exists_in_queue = delays_queue.exists(queue_name, order_id)
    if exists_in_queue == order.id: 
        return JsonResponse({'message': 'The order is already in the delay queue'}, status=400)

    # Check if there's a related trip with the order
    if Trip.objects.filter(status__in=['VENDOR_AT', 'ASSIGNED', 'PICKED'],order=order).exists():

        # Call the external API to get a new delivery estimate
        response = requests.get('https://run.mocky.io/v3/122c2796-5df4-461c-ab75-87c1192b17f7')
        if response.status_code == 200:
            new_estimated_delivery = response.json().get('data').get('eta')

            # Update the order with the new estimated delivery time
            order.eta += new_estimated_delivery
            order.save()


            report = DelayReport(order=order)
            report.save()

            return JsonResponse({'message': f'Order updated with new estimated time and the report has been submitted. Your order will arrive at {order.time_stamp + timedelta(minutes=order.delivery_time)}', 'new_estimated_time':new_estimated_delivery, 'report_id':report.id}, status=201)
        else:
            return JsonResponse({'message': 'Failed to get new estimated time'}, status=500)
        


    else:
        report = DelayReport(order=order)
        report.save()
        
        if order.status != 'INVESTIGATING':
            order.status = 'DELAYED'
            order.save()

            # Enqueue the delayed order to the delays_queue
            delays_queue.enqueue(queue_name, order.id)

            return JsonResponse({'message': 'Order put in delay queue'})
        return JsonResponse({'message':'Your delay report has been submitted'})
    
@api_view(['GET'])
def assign_report(request,agent_id):

    if Order.objects.filter(status='INVESTIGATING',agent_id=agent_id).exists():
        return JsonResponse({'message':'This agent has already been assigned a report'},status=400)
    
    if delays_queue.count(queue_name) == 0:
        return JsonResponse({'message': 'No reports available'}, status=200)

    
    try:
        order_id = delays_queue.dequeue(queue_name)
        order = Order.objects.get(id=order_id)
        order.status = 'INVESTIGATING'
        order.agent_id = agent_id
        order.save()

        return JsonResponse({'message':'Delayed order assigned succesfully','order_id':order.id})

    except DelayReport.DoesNotExist:
        return JsonResponse({'message': 'No such order exists'}, status=404)
