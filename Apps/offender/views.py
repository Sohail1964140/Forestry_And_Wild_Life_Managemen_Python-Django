from django.shortcuts import render,HttpResponse
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
from .models import Offender
from .forms import offenderForm
from Apps.core.views import hx_Redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def get_template(request, name):
    
    if request.htmx:
        return f'offender/partials/{name}.html'
    
    return f'offender/{name}.html'


"""
OFFENDER CREATE VIEW
"""
class offenderAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': offenderForm(),'heading':'Add Offender'}
        template = get_template(request, 'offender_add')
        return render(request,template, context )
    
    
    def post(self, request):
    
        form = offenderForm(data=request.POST)
        if form.is_valid():
            
            offender = form.save()
            form = offenderForm()
            
            messages.success(request, "Offender Addedd Successfully")
            return hx_Redirect("offenderList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'offender_add')
        
        context = {'form': form}
        return render(request,template, context)
    
    
"""
OFFENDER LIST VIEW
"""
class offenderListView(LoginRequiredMixin,ListView):
    
    model = Offender
    context_object_name = 'offenders'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'offender_list')
    
    def get_queryset(self):
        return Offender.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(offenderListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(offenderListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context


"""
OFFENDER SEARCH VIEW
"""
class offenderSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        offenders = Offender.objects.filter(Q(name__istartswith=query)  | Q(contact__istartswith=query)).order_by('pk')
        paginator = Paginator(offenders, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'offenders': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(request,'offender_list'), 'table', context)
        
        
        return HttpResponse(response)
    
"""
OFFENDER UPDATE VIEW
"""
class offenderUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, pk):
        
        offender = get_object_or_404(Offender, pk=pk)
        form = offenderForm(instance=offender)
        context = {'form':form, 'heading':'Update Offender','isUpdate':True, 'object': offender}
        template_name = get_template(request, 'offender_add')
        
        return render(request, template_name, context)
    
    def post(self, request, pk):
        
        offender = get_object_or_404(Offender, pk=pk)
        form = offenderForm(instance=offender, data=request.POST)
        
        if form.is_valid():
            
            offender = form.save()
            messages.success(request, f'{offender} Update Successfully')
            return hx_Redirect("offenderList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Offender','isUpdate':True, 'object': offender}
        template_name = get_template(request, 'offender_add')
        
        return render(request,template_name, context)



"""
OFFENDER DELETE VIEW
"""

class offenderDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, pk):
       
        try:
            
            offender = get_object_or_404(Offender, pk=pk)
            
            context = {'object': offender, 'msg': f'Are you sure you want to delete  <strong> <i>{offender.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete'), context)
        

        except Http404:
            
            return render(request, get_template(request, '404')) 
    
    
    
    def post(self, request, pk):
        
        offender = get_object_or_404(Offender, pk=pk)
        offender.delete()
        messages.success(request, "Offender Deleted Successfully")
        return hx_Redirect("offenderList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete'), context)