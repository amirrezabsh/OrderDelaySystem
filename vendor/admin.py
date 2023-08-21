from django.contrib import admin
from .models import Order, DelayReport, Trip, Vendor
# Register your models here.

admin.site.register(Order)
admin.site.register(DelayReport)
admin.site.register(Trip)
admin.site.register(Vendor)
