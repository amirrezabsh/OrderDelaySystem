from django.db.models import Max, F, FloatField, Q, ExpressionWrapper, OuterRef, Subquery, Sum
from .models import Vendor
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import Cast, Coalesce
from collections import defaultdict
class VendorService:
    @staticmethod
    # Service to get the list of vendors ordered by their total delays for the past week
    def get_weekly_vendors_data():
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        # The main query to get list of vendors
        vendors_data = Vendor.objects.annotate(
            latest_delay_report_time=Max('order__delayreport__time_stamp', filter=Q(order__time_stamp__gte=seven_days_ago)),
            total_delay_duration=ExpressionWrapper(
                (F('latest_delay_report_time') - F('order__time_stamp')) / 60000000 - (F('order__delivery_time') + F('order__eta')),
                output_field=FloatField()
            ),
            
        ).filter(total_delay_duration__isnull=False).values('id', 'name', 'total_delay_duration')

        # Group by vendor ID and sum total_delay_duration
        vendors_data = list(vendors_data)

        # Create a defaultdict to store the sums for each ID
        sums_by_id = defaultdict(float)

        # Iterate through the list and calculate sums
        for item in vendors_data:
            id_value = item['id']
            value = item['total_delay_duration']
            sums_by_id[id_value] += value

        # Convert the defaultdict to a list of dictionaries
        result_list = [{'id': id_value, 'total_delay_duration_sum': sum_value} for id_value, sum_value in sums_by_id.items()]

        return result_list
