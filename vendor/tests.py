from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from .models import Vendor
from order.models import Order, DelayReport

class WeeklyVendorsTestCase(TestCase):
    def setUp(self):
        # Create sample data
        self.vendor = Vendor.objects.create(name='Vendor A')
        self.order = Order.objects.create(vendor=self.vendor, delivery_time=30, eta=10,time_stamp=timezone.now() - timedelta(minutes=65))
        self.delay_report = DelayReport.objects.create(order=self.order)
        self.client = APIClient()

    def test_weekly_vendors_endpoint(self):
        response = self.client.get('/api/vendor/weekly-vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['orders']), 1)

    def test_weekly_vendors_data(self):
        response = self.client.get('/api/vendor/weekly-vendors/')
        vendor_data = response.data['orders'][0]
        self.assertEqual(vendor_data['id'], self.vendor.id)
        self.assertGreaterEqual(vendor_data['total_delay_duration_sum'], 20.0)

    def test_weekly_vendors_without_delay_report(self):
        self.delay_report.delete()  # Delete the delay report
        response = self.client.get('/api/vendor/weekly-vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['orders']), 0)

    def test_weekly_vendors_no_orders(self):
        self.order.delete()  # Delete the order
        response = self.client.get('/api/vendor/weekly-vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['orders']), 0)

    def test_weekly_vendors_with_old_order(self):
        # Create an old order that doesn't meet the 7-day requirement
        old_order = Order.objects.create(vendor=self.vendor, delivery_time=30, eta=10,
                                         time_stamp=timezone.now() - timedelta(days=8))
        DelayReport.objects.create(order=old_order)
        response = self.client.get('/api/vendor/weekly-vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['orders']), 1)
