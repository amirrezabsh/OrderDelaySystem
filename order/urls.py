
from django.urls import path
from vendor import views

urlpatterns = [
    path('report-delay/<int:order_id>/', views.report_delay, name='report_delay'),
    path('assign-report/<int:agent_id>/', views.assign_report, name='assign_report'),
]