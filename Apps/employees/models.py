from django.db import models
from django.utils.text import slugify
from Apps.core.models import ForestArea, DESIGNATION
# Create your models here.




class EMPLOYEE(models.Model):
    
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, blank=False, null=False, unique=True)
    address = models.TextField(max_length=80)
    contact = models.CharField(max_length=15)
    image = models.ImageField(upload_to="employee/images/")
    designation = models.ForeignKey(to=DESIGNATION, on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.name
    


class VISIT(models.Model):
    
    forestArea = models.ForeignKey(to=ForestArea, on_delete=models.CASCADE, related_name="visits")
    date = models.DateField()
    description = models.TextField()
    employees = models.ManyToManyField(to=EMPLOYEE, related_name="visits")

