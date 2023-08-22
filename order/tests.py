from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from .services import DelayService, AssignmentService
from .models import Order, DelayReport, Vendor, Trip
from .views import report_delay, assign_report
from .utils import OrderStatus, TripStatus
from datetime import timedelta
from django.utils import timezone

class ReportDelayTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.service = DelayService()

        self.order = Order.objects.create(vendor_id=1, delivery_time=30, eta=10,time_stamp=timezone.now() - timedelta(minutes=40))
        self.vendor = Vendor.objects.create(name='digikala')
        self.delay_report = DelayReport.objects.create(order=self.order)

    def test_report_delay_successful(self):
        request = self.factory.get(f'/api/order/report-delay/{self.order.id}/')
        response = report_delay(request, self.order.id)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)


class AssignReportTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.agent_id = 1
        self.order = Order.objects.create(vendor_id=1, delivery_time=30, eta=10)
        self.vendor = Vendor.objects.create(name='digikala')
        self.delay_report = DelayReport.objects.create(order=self.order)

    def test_assign_report_successful(self):
        request = self.factory.get(f'/api/order/assign-report/{self.agent_id}/')
        response = assign_report(request, self.agent_id)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)

    def test_assign_report_no_reports_available(self):
        # Delete the delay report to make no reports available
        self.delay_report.delete()

        request = self.factory.get(f'/api/order/assign-report/{self.agent_id}/')
        response = assign_report(request, self.agent_id)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)

    def test_assign_report_agent_already_assigned(self):
        # Assign the report to the agent
        self.order.agent_id = self.agent_id
        self.order.status = OrderStatus.INVESTIGATING
        self.order.save()

        request = self.factory.get(f'/api/order/assign-report/{self.agent_id}/')
        response = assign_report(request, self.agent_id)

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)

