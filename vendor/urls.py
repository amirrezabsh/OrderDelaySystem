from django.urls import path
from vendor import views

urlpatterns = [


    path('weekly-vendors/', views.weekly_vendors, name='weekly_vendors'),

]
