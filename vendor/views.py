from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.db.models import OuterRef, Subquery, Count, Sum, DecimalField, Q, ExpressionWrapper, IntegerField, DurationField, F, Max, FloatField, DateTimeField
from .models import Vendor
from order.models import DelayReport
from redis_utils import RedisQueue, QueueNames
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from django.db.models.functions import Cast, Coalesce

# Get the singleton instance of DelaysQueue
delays_queue = RedisQueue()
queue_name = QueueNames.DELAYS


@api_view(['GET'])
def weekly_vendors(request):
    seven_days_ago = timezone.now() - timedelta(days=7)
    delay = DelayReport.objects.get(id=26)
    print((delay.time_stamp - delay.order.time_stamp).total_seconds())

    vendors_data = Vendor.objects.annotate(
        latest_delay_report_time=Max('order__delayreport__time_stamp', filter=Q(order__time_stamp__gte=seven_days_ago)),
        total_delay_duration=ExpressionWrapper(
            (F('latest_delay_report_time') - F('order__time_stamp')) / 60000000 - (F('order__delivery_time') + F('order__eta')),
            output_field=FloatField()
        )
    ).values('id', 'name', 'total_delay_duration')

    return JsonResponse({'orders': list(vendors_data)})


