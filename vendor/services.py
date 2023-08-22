from django.db.models import Max, F, FloatField, Q, ExpressionWrapper
from .models import Vendor
from django.utils import timezone
from datetime import timedelta

class VendorService:
    @staticmethod
    def get_weekly_vendors_data():
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        vendors_data = Vendor.objects.annotate(
            latest_delay_report_time=Max('order__delayreport__time_stamp', filter=Q(order__time_stamp__gte=seven_days_ago)),
            total_delay_duration=ExpressionWrapper(
                (F('latest_delay_report_time') - F('order__time_stamp')) / 60000000 - (F('order__delivery_time') + F('order__eta')),
                output_field=FloatField()
            )
        ).values('id', 'name', 'total_delay_duration')

        return list(vendors_data)
