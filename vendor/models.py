# vendor/models.py
from django.db import models
from datetime import timedelta
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    STATUS_CHOICES = [
        ('DELAYED', 'Delayed'),
        ('INVESTIGATING', 'Investigating'),
        ('FOLLOWING_UP', 'Following Up'),
        ('DONE','Done'),
        ('OPEN', 'Open')
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,blank=False,null=False)
    agent_id = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='OPEN')
    delivery_time = models.PositiveIntegerField(blank=False,null=False)
    eta = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(default=timezone.now()) # Instead of auto_now_add=True used default=timezone.now() for simplicity



class Trip(models.Model):
    STATUS_CHOICES = [
        ('DELIVERED', 'Delivered'),
        ('PICKED', 'Picked'),
        ('AT_VENDOR', 'At Vendor'),
        ('ASSIGNED', 'Assigned'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

class DelayReport(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False)
    time_stamp = models.DateTimeField(default=timezone.now()) # Instead of auto_now_add=True used default=timezone.now() for simplicity
