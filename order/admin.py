from django.contrib import admin
from .models import Order, DelayReport, Trip
# Register your models here.
admin.site.register(Order)
admin.site.register(DelayReport)
admin.site.register(Trip)