from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return f"Name: {self.name} with {self.id} id"