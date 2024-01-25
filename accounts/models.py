from django.db import models
from django.contrib.auth.models import AbstractUser
from Apps.employees.models import EMPLOYEE
# Create your models here.

class USER(AbstractUser):
    
    employee = models.OneToOneField(to=EMPLOYEE, on_delete=models.CASCADE, null=True, blank=True)
