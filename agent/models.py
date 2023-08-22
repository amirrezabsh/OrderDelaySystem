from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=30)
    