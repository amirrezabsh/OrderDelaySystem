from django.shortcuts import render
from .models import Agent
from django.http import JsonResponse
from redis_utils import RedisQueue
from vendor.models import DelayReport
# Get the singleton instance of DelaysQueue
delays_queue = RedisQueue()
delays_queue_name = 'delays'
# Create your views here.

def assign_report(request,agent_id):
    try:
        agent = Agent.objects.get(id=agent_id)
    except Agent.DoesNotExist:
        return JsonResponse({'message':'No such agent exists'},status=404)
    if delays_queue.count(delays_queue_name) == 0:
        return JsonResponse({'message':'Delays report queue is empty'}, status=200)
    try:
        report = DelayReport.objects.get(id=delays_queue.dequeue(delays_queue_name))
        report.agent = agent
        report.save()
    except DelayReport.DoesNotExist:
        return JsonResponse({'message':'No such report exists'},status=500)