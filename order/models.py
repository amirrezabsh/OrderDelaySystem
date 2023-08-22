from django.db import models
from django.utils import timezone
from vendor.models import Vendor

# Create your models here.

class Order(models.Model):
    # Choices for order status
    STATUS_CHOICES = [
        ('DELAYED', 'Delayed'),
        ('INVESTIGATING', 'Investigating'),
        ('FOLLOWING_UP', 'Following Up'),
        ('DONE','Done'),
        ('OPEN', 'Open')
    ] 
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,blank=False,null=False) # A Many-To-One relationship between Order and Vendor model
    agent_id = models.IntegerField(null=True,blank=True) # This should be a foreign key to Agent model but for simplicity we just consider a simple Integer field
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='OPEN') # Indicates the status of the order
    delivery_time = models.PositiveIntegerField(blank=False,null=False) # The initial estimated time for the order
    eta = models.IntegerField(default=0) # New estimated time in case the order is delayed
    time_stamp = models.DateTimeField(default=timezone.now()) # Instead of auto_now_add=True used default=timezone.now() for simplicity



class Trip(models.Model):
    # Choices for trip status
    STATUS_CHOICES = [
        ('DELIVERED', 'Delivered'),
        ('PICKED', 'Picked'),
        ('AT_VENDOR', 'At Vendor'),
        ('ASSIGNED', 'Assigned'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE) # A One-To-One relationship between Trip and Order models
    status = models.CharField(max_length=20, choices=STATUS_CHOICES) # Trip status

class DelayReport(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False) # A Many-To-One relationship between DelayReport model and Order model
    time_stamp = models.DateTimeField(default=timezone.now()) # Instead of auto_now_add=True used default=timezone.now() for simplicity
