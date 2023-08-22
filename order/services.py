from django.utils import timezone
import requests
from datetime import timedelta
from .models import Order, Trip, DelayReport
from redis_utils import RedisQueue, QueueNames
from .utils import OrderStatus, TripStatus

delays_queue = RedisQueue()
queue_name = QueueNames.DELAYS

class DelayService:
    @staticmethod
    def report_delay(order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return 'Order not found', 404, None
        
        current_time = timezone.now()
        if timedelta(minutes=(order.delivery_time + order.eta)) + order.time_stamp > current_time:
            return 'Cannot report delay before the estimated delivery time has passed', 400, None
        
        exists_in_queue = delays_queue.exists(queue_name, order_id)
        if exists_in_queue == order.id: 
            return 'The order is already in the delay queue', 400, None
        
        if Trip.objects.filter(status__in=[TripStatus.AT_VENDOR, TripStatus.ASSIGNED, TripStatus.PICKED], order=order).exists():
            response = requests.get('https://run.mocky.io/v3/122c2796-5df4-461c-ab75-87c1192b17f7')
            if response.status_code == 200:
                new_estimated_delivery = response.json().get('data').get('eta')
                order.eta += new_estimated_delivery
                order.save()
                report = DelayReport(order=order)
                report.save()
                return f'Order updated with new estimated time and the report has been submitted. Your order will arrive at {order.time_stamp + timedelta(minutes=order.delivery_time)}', 201, new_estimated_delivery
            
            return 'Failed to get new estimated time', 500, None
        else:
            report = DelayReport(order=order)
            report.save()
            if order.status != OrderStatus.INVESTIGATING:
                order.status = OrderStatus.DELAYED
                order.save()
                delays_queue.enqueue(queue_name, order.id)
            return  'Order put in delay queue', 200, None

class AssignmentService:
    @staticmethod
    def assign_report(agent_id):
        if Order.objects.filter(status=OrderStatus.INVESTIGATING, agent_id=agent_id).exists():
            return 'This agent has already been assigned a report', 400
        
        if delays_queue.count(queue_name) == 0:
            return 'No reports available', 200
        
        try:
            order_id = delays_queue.dequeue(queue_name)
            order = Order.objects.get(id=order_id)
            order.status = OrderStatus.INVESTIGATING
            order.agent_id = agent_id
            order.save()
            return 'Delayed order assigned succesfully', 200
        except Order.DoesNotExist:
            return 'No such order exists', 404
