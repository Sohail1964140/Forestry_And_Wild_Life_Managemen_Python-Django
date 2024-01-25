from django.shortcuts import render,HttpResponse
from .forms import empForm, visitForm
from .models import EMPLOYEE, VISIT
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from time import sleep
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from render_block import render_block_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.db import transaction
from Apps.core.views import hx_Redirect
from Apps.core.models import ForestArea
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def get_template(request, name, path="employee"):
    
    if request.htmx:
        return f'{path}/partials/{name}.html'
    
    return f'{path}/{name}.html'


"""
EMPLOYEE CREATE VIEW
"""
class empAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': empForm(),'heading':'Add Employee'}
        template = get_template(request, 'emp_add')
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = empForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            
            emp = form.save()
            form = empForm()
            
            messages.success(request, "Employee Addedd Successfully")
            
            return hx_Redirect("employee:empList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'emp_add')
        
        context = {'form': form}
        return render(request,template, context)
    
    
"""
EMPLOYEE LIST VIEW
"""
class empListView(LoginRequiredMixin,ListView):
    
    model = EMPLOYEE
    context_object_name = 'employees'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'emp_list')
    
    def get_queryset(self):
        return EMPLOYEE.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(empListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(empListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context


"""
EMPLOYEE Search VIEW
"""
class empSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        employees = EMPLOYEE.objects.filter(Q(name__istartswith=query) | Q(email__istartswith=query) | Q(contact__istartswith=query)).order_by('pk')
        paginator = Paginator(employees, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'employees': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(request,'emp_list'), 'table', context)
        
        
        return HttpResponse(response)
    
"""
EMPLOYEE Udate VIEW
"""
class empUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, pk):
        
        employee = get_object_or_404(EMPLOYEE, pk=pk)
        form = empForm(instance=employee)
        context = {'form':form, 'heading':'Update Employee','isUpdate':True, 'object': employee}
        template_name = get_template(request, 'emp_add')
        
        return render(request, template_name, context)
    
    def post(self, request, pk):
        
        employee = get_object_or_404(EMPLOYEE, pk=pk)
        form = empForm(instance=employee, data=request.POST, files=request.FILES)
        
        if form.is_valid():
            
            employee = form.save()
            messages.success(request, f'{employee} Update Successfully')
            return hx_Redirect("employee:empList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Employee','isUpdate':True, 'object': employee}
        template_name = get_template(request, 'emp_add')
        
        return render(request,template_name, context)


    
"""
EMPLOYEE DELETE VIEW
"""

class empDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, pk):
       
        try:
            
            employee = get_object_or_404(EMPLOYEE, id=pk)
            
            context = {'object': employee, 'msg': f'Are you sure you want to delete  <strong> <i>{employee.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete'), context)
        

        except Http404:
            
            
            return render(request, get_template(request, '404')) 
    
    
    
    def post(self, request, pk):
        
        

        employee = get_object_or_404(EMPLOYEE, id=pk)
        
        employee.delete()       
        messages.success(request, "Employee Deleted Successfully")
        context = {
            'isDeleted':True
        }
        return hx_Redirect("employee:empList")
    
    

"""
-<( === === === === === === === === === === === === VISITS  === === === === === === === === === === === === )>-
"""


"""
VISIT CREATE VIEW
"""
class visitAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': visitForm(),'heading':'Add Visit'}
        template = get_template(request,path="visit" ,name='visit_add')
        return render(request,template, context )
    
    
    def post(self, request):
        
        form = visitForm(data=request.POST)
        
        if form.is_valid():
            visit = form.save()
            form = visitForm()
            messages.success(request, "Visits Addedd Successfully")
            return hx_Redirect("employee:visitList")
        else:
            messages.error(request, "Please Correct the error bellow")
            
        template = get_template(request,path="visit" ,name='visit_add')
        
        context = {'form': form,'heading':'Add Visit'}
        return render(request,template, context)
    


"""
VISIT LIST VIEW
"""
class visitListView(LoginRequiredMixin,ListView):
    
    model = VISIT
    context_object_name = 'visits'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, name='visit_list', path="visit")
    
    def get_queryset(self):
        return VISIT.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(visitListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(visitListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context["areas"] = ForestArea.objects.all()
        return context
    


"""
VISIT UPDATE VIEW
"""
class visitUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, pk):
        
        visit = get_object_or_404(VISIT, pk=pk)
        form = visitForm(instance=visit)
    
        context = {'form':form, 'heading':'Update Visits',
                   'isUpdate':True, 
                   'object': visit,
                   }
        template_name = get_template(request, name='visit_add', path="visit")
        
        return render(request, template_name, context)
    
    def post(self, request, pk):
        
        visit = get_object_or_404(VISIT, pk=pk)
        form = visitForm(instance=visit, data=request.POST)

        if form.is_valid():
            
            visit = form.save()                
                
            messages.success(request, f'{visit} Update Successfully')
            return hx_Redirect("employee:visitList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
            
        
        
        context = {'form':form, 'heading':'Update Visit',
                   'isUpdate':True,
                   'object': visit
                   }
        
        template_name = get_template(request, 'visit_add', path="visit")
        
        return render(request,template_name, context)



"""
VISTI DELETE VIEW
"""

class visitDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, pk):
       
        try:
            
            visit = get_object_or_404(VISIT, pk=pk)
            
            context = {'object': visit, 'msg': f'Are you sure you want to delete  <strong> <i>{visit}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete',path="visit"), context)
        

        except Http404:
            
            return render(request, get_template(request, '404', path="visit")) 
    
    
    
    def post(self, request, pk):
        
        visit = get_object_or_404(VISIT, pk=pk)
        visit.delete()
        messages.success(request, "Visit Deleted Successfully")
        context = {
            'isDeleted':True
        }
        return hx_Redirect("employee:visitList")
        # return render(request, get_template(request, 'delete', path="visit"), context)