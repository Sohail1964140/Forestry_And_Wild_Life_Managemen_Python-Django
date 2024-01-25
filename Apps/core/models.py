from django.db import models
from django.utils.text import slugify
# Create your models here.



class ForestArea(models.Model):
    
    name = models.CharField(max_length = 30, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(max_length=200)
    slug = models.SlugField(unique=True,blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ForestArea, self).save(args, kwargs)
    
    class Meta:
        ordering = ['pk']


class TreeSpecies(models.Model):
    
    name = models.CharField(max_length = 30, unique=True)
    description = models.TextField(max_length=200)
    slug = models.SlugField(unique=True,blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        
        
        self.slug = slugify(self.name)
        super(TreeSpecies, self).save(args, kwargs)
    
    class Meta:
        ordering = ['pk']

class CUSTOMER(models.Model):
    
    name = models.CharField(max_length=30)
    address = models.TextField(max_length=80)
    contact = models.CharField(max_length=11)
    image = models.ImageField(upload_to="customer/images/")
    
    def __str__(self):
        
        return self.name
    
    class Meta:
        ordering = ['pk']
    

class DESIGNATION(models.Model):

    name = models.CharField(max_length=30)

    
    def __str__(self):
        
        return self.name