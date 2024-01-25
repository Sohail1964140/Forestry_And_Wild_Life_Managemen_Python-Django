from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from Apps.core.models import ForestArea
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Apps.employees.models import EMPLOYEE
from Apps.complaints.models import Complaints
from Apps.incomeExpence.models import Income
from Apps.incomeExpence.models import Expense
from django.db.models import Sum
from Apps.wood.models import WoodEntry

class homeView(TemplateView):
    
    def get_template_names(self, *args, **kwargs):
        
        if self.request.user.is_authenticated:

            return  'base.html'
        
        return "index.html"

    def get_context_data(self):
       
        ForestAreas = list(ForestArea.objects.values('name', 'latitude', 'longitude'))
        context = super().get_context_data()
        context['forestArea'] = ForestAreas
        context['countEmployies'] = EMPLOYEE.objects.all().count()
        context['countActiveComplaints'] = Complaints.objects.filter(status=1).count()
        incom =  Income.objects.aggregate(total=Sum('amount'))['total'] or 0 
        wIncom = WoodEntry.objects.aggregate(total=Sum('fineAmount'))['total'] or 0
        context['totalIncom'] = incom + wIncom
        context['totalExpenses'] = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        
        return context