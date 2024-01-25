from django.db import models
from Apps.offender.models import Offender
from Apps.core.models import ForestArea, TreeSpecies, CUSTOMER
from django.utils.timezone import now
# Create your models here.



class WoodEntry(models.Model):
    
    area = models.ForeignKey(to=ForestArea, on_delete=models.SET_NULL, related_name="woods", null=True)
    species = models.ForeignKey(to=TreeSpecies, on_delete=models.SET_NULL, related_name="woods", null=True)
    offender = models.ForeignKey(to=Offender, on_delete=models.SET_NULL, related_name="woods", null=True)
    quantity = models.PositiveIntegerField()
    fineAmount = models.IntegerField()
   
    date = models.DateField(default=now)
    description = models.TextField(max_length=200, null=True, blank=True)
        
        

class WoodAuction(models.Model):
    
    wood = models.ForeignKey(to=WoodEntry, on_delete=models.CASCADE, related_name="auction" )
    customer = models.ForeignKey(to=CUSTOMER, on_delete=models.CASCADE, related_name="auctions")
    price = models.PositiveIntegerField()
   
    date = models.DateField(default=now)
    description = models.TextField(max_length=200, null=True, blank=True)


class TreeAltment(models.Model):
    
    area = models.ForeignKey(to=ForestArea, on_delete=models.SET_NULL, related_name="altments", null=True)
    species = models.ForeignKey(to=TreeSpecies, on_delete=models.SET_NULL, related_name="altments", null=True)
    customer = models.ForeignKey(to=CUSTOMER, on_delete=models.CASCADE, related_name="altments")
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    date = models.DateField(default=now)
    description = models.TextField(max_length=200, null=True, blank=True)