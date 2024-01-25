from django.contrib import admin
from .models import ForestArea
# Register your models here.

@admin.register(ForestArea)
class forestAreaAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'latitude','longitude', 'description', 'slug')
