from django.urls import path
from vendor import views

app_name = 'vendors'

urlpatterns = [
    path('report-delay/<int:order_id>/', views.report_delay, name='report_delay'),
]
