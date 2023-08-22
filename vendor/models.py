# vendor/models.py
from django.db import models
from datetime import timedelta
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=100)

 