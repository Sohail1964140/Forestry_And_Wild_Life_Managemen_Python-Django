from django.db import models
from django.utils.text import slugify
from django.urls import reverse_lazy as _
from django.db.models import Sum
from datetime import datetime
from django.utils.timezone import now
# Create your models here.

class IncomeSource(models.Model):
    
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    
    
    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.name)
        
        super(IncomeSource, self).save(args, kwargs)


class Income(models.Model):
    
    source = models.ForeignKey(to="IncomeSource", on_delete=models.CASCADE, related_name="incoms")
    amount = models.IntegerField()
    date = models.DateField(default=now)
    description = models.TextField(max_length=200, null=True, blank=True)

    @property
    def getTotal(self):
        
        return Income.objects.aggregate(total=Sum('amount'))['total']
        
        


class ExpenseSource(models.Model):
    
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    
    
    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.name)
        
        super(ExpenseSource, self).save(args, kwargs)


class Expense(models.Model):
    
    source = models.ForeignKey(to="ExpenseSource", on_delete=models.CASCADE, related_name="expenses")
    amount = models.IntegerField()
    date = models.DateField(default=now)
    description = models.TextField(max_length=200, null=True, blank=True)
    
    @property
    def getTotal(self):
        
        return Expense.objects.aggregate(total=Sum('amount'))['total']