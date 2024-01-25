from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(EMPLOYEE)
class empAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'email', 'address', 'contact', 'designation','image')