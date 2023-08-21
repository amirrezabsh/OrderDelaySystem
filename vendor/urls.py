from django.urls import path
from vendor import views

urlpatterns = [
    path('report-delay/<int:order_id>/', views.report_delay, name='report_delay'),
    path('weekly-vendors/', views.weekly_vendors, name='weekly_vendors')
]
