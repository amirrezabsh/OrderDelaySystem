# vendor/models.py
from django.db import models
from agent.models import Agent

class Vendor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} with {self.id} id"

class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,blank=False,null=False)
    delivery_time = models.DurationField(blank=False,null=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.vendor}: {self.time_stamp}"

class Trip(models.Model):
    STATUS_CHOICES = [
        ('DELIVERED', 'Delivered'),
        ('PICKED', 'Picked'),
        ('VENDOR_AT', 'Vendor At'),
        ('ASSIGNED', 'Assigned'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self) -> str:
        return f"order: {self.order.id}, status: {self.status}"

class DelayReport(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False)
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, blank=True, null=True)
    is_checked = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"order: {self.order.id}, status: {self.is_checked}, agent: {self.agent.id}"