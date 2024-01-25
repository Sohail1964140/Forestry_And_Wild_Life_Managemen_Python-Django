from django.contrib import admin
from . models import IncomeSource, ExpenseSource, Income, Expense

# Register your models here.

@admin.register(IncomeSource)
class IncomeSourceAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'slug')
    
    

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    
    list_display = ('source', 'amount', 'date', 'description')
    

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    
    list_display = ('source', 'amount', 'date', 'description')