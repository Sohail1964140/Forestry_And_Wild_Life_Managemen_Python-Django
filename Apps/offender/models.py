from django.db import models
from django.utils.timezone import now
# Create your models here.
class Offender(models.Model):
    
    name = models.CharField(max_length=30)
    address = models.TextField(max_length=60)
    date = models.DateField(default=now)
    contact = models.CharField(max_length=11)
    
    def __str__(self):
        
        return f"{self.name} - {self.contact}"
    