# vendor/models.py
from django.db import models
from agent.models import Agent
class Vendor(models.Model):
    name = models.CharField(max_length=100)

class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    delivery_time = models.TimeField()
    time_stamp = models.DateTimeField(auto_now_add=True)

class Trip(models.Model):
    STATUS_CHOICES = [
        ('DELIVERED', 'Delivered'),
        ('PICKED', 'Picked'),
        ('VENDOR_AT', 'Vendor At'),
        ('ASSIGNED', 'Assigned'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class DelayReport(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
