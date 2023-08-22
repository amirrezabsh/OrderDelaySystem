from django.shortcuts import render
from .models import Agent
from django.http import JsonResponse
from redis_utils import RedisQueue
from vendor.models import DelayReport, Order
from rest_framework.decorators import api_view
# Get the singleton instance of DelaysQueue
delays_queue = RedisQueue()
delays_queue_name = 'delays'
# Create your views here.


