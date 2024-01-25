from django.shortcuts import render,HttpResponse
from .forms import forestAreaForm, specieForm, customerForm, designationForm
from .models import ForestArea, TreeSpecies, CUSTOMER, DESIGNATION
from django.views import View
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from time import sleep
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from render_block import render_block_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def get_template(request, name, path="forestArea"):
    
    if request.htmx:
        return f'{path}/partials/{name}.html'
    
    return f'{path}/{name}.html'

def hx_Redirect(url):
    resp = HttpResponseRedirect(_(url))
    resp['HX-Redirect'] = _(url)
    return resp


"""
Area CREATE VIEW
"""
class areaAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': forestAreaForm(),'heading':'Add Area'}
        template = get_template(request, 'area_add')
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = forestAreaForm(data=request.POST)
        if form.is_valid():
            
            emp = form.save()
            form = forestAreaForm()
            
            messages.success(request, "Area Addedd Successfully")
            return hx_Redirect("core:areaList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'area_add')
        
        context = {'form': form}
        return render(request,template, context)
    
    
"""
AREA LIST VIEW
"""
class areaListView(LoginRequiredMixin,ListView):
    
    model = ForestArea
    context_object_name = 'areas'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'area_list')
    
    def get_queryset(self):
        return ForestArea.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(areaListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(areaListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context


"""
Area Search VIEW
"""
class areaSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        areas = ForestArea.objects.filter(Q(name__istartswith=query)).order_by('pk')
        paginator = Paginator(areas, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'areas': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(request,'area_list'), 'table', context)
        
        
        return HttpResponse(response)
    
"""
Area Udate VIEW
"""
class areaUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, slug):
        
        area = get_object_or_404(ForestArea, slug=slug)
        form = forestAreaForm(instance=area)
        context = {'form':form, 'heading':'Update Area','isUpdate':True, 'object': area}
        template_name = get_template(request, 'area_add')
        
        return render(request, template_name, context)
    
    def post(self, request, slug):
        
        area = get_object_or_404(ForestArea, slug=slug)
        form = forestAreaForm(instance=area, data=request.POST)
        
        if form.is_valid():
            
            area = form.save()
            messages.success(request, f'{area} Update Successfully')
            return hx_Redirect("core:areaList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Area','isUpdate':True, 'object': area}
        template_name = get_template(request, 'area_add')
        
        return render(request,template_name, context)


    
"""
Area Delete VIEW
"""

class areaDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, slug):
       
        try:
            
            area = get_object_or_404(ForestArea, slug=slug)
            
            context = {'object': area, 'msg': f'Are you sure you want to delete  <strong> <i>{area.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete'), context)
        

        except Http404:
            
            
            return render(request, get_template(request, '404')) 
    
    
    
    def post(self, request, slug):
        
        
        
        area = get_object_or_404(ForestArea, slug=slug)

        area.delete()
        messages.success(request, f'{area.name} deleted successfully')

        return hx_Redirect("core:areaList")
        # context = {'isDeleted': True,'msg': f'{area.name} deleted Successfully'}
        # return render(request, get_template(request, 'delete'), context)
    
    

"""
****************************************** TREE SPECIE SECTION ******************************************
"""

"""
Tree Specie CREATE VIEW
"""
class specieAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': specieForm(),'heading':'Add Specie'}
        template = get_template(request, 'specie_add', path="treeSpecies")
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = specieForm(data=request.POST)
        if form.is_valid():
            
            specie = form.save()
            form = specieForm()
            
            messages.success(request, "Specie Addedd Successfully")
            return hx_Redirect("core:specieList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'specie_add', path="treeSpecies")
        
        context = {'form': form}
        return render(request,template, context)
    
    
"""
Tree Specie LIST VIEW
"""
class specieListView(LoginRequiredMixin,ListView):
    
    model = ForestArea
    context_object_name = 'species'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'specie_list', path="treeSpecies")
    
    def get_queryset(self):
        return TreeSpecies.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(specieListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(specieListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context


"""
Tree Specie Search VIEW
"""
class specieSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        species = TreeSpecies.objects.filter(Q(name__istartswith=query)).order_by('pk')
        paginator = Paginator(species, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'species': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(request,'specie_list', path="treeSpecies"), 'table', context)
        
        
        return HttpResponse(response)
    
"""
Tree Specie Udate VIEW
"""
class specieUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, slug):
        
        specie = get_object_or_404(TreeSpecies, slug=slug)
        form = specieForm(instance=specie)
        context = {'form':form, 'heading':'Update Specie','isUpdate':True, 'object': specie}
        template_name = get_template(request, 'specie_add', path="treeSpecies")
        
        return render(request, template_name, context)
    
    def post(self, request, slug):
        
        specie = get_object_or_404(TreeSpecies, slug=slug)
        form = specieForm(instance=specie, data=request.POST)
        
        if form.is_valid():
            
            specie = form.save()
            messages.success(request, f'{specie} Update Successfully')
            return hx_Redirect("core:specieList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Specie','isUpdate':True, 'object': specie}
        template_name = get_template(request, 'specie_add', path="treeSpecies")
        
        return render(request,template_name, context)


    
"""
Tree Specie Delete VIEW
"""

class specieDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, slug):
       
        try:
            
            specie = get_object_or_404(TreeSpecies, slug=slug)
            
            context = {'object': specie, 'msg': f'Are you sure you want to delete  <strong> <i>{specie.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete', path="treeSpecies"), context)
        

        except Http404:
            
            
            return render(request, get_template(request, '404', path="treeSpecies")) 
    
    
    
    def post(self, request, slug):
        

        specie = get_object_or_404(TreeSpecies, slug=slug)

        specie.delete()
        messages.success(request, f'{specie.name} deleted successfully')

        return hx_Redirect("core:specieList")
        
        # context = {'isDeleted': True,'msg': f'{specie.name} deleted Successfully'}
        # return render(request, get_template(request, 'delete', path="treeSpecies"), context)




"""
****************************************** CUSTOMER SECTION ******************************************
"""

"""
CUSTOMER CREATE VIEW
"""
class customerAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': customerForm(),'heading':'Add Customer'}
        template = get_template(request, 'customer_add', path="customer")
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = customerForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            
            customer = form.save()
            form = customerForm()
            
            messages.success(request, "Customer Addedd Successfully")
            return hx_Redirect("core:customerList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'customer_add', path="customer")
        
        context = {'form': form}
        return render(request,template, context)
    
        
"""
CUSTOMER LIST VIEW
"""
class customerListView(LoginRequiredMixin,ListView):
    
    model = CUSTOMER
    context_object_name = 'customers'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'customer_list', path="customer")
    
    def get_queryset(self):
        return CUSTOMER.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(customerListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(customerListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context


"""
CUSTOMER SEARCH VIEW
"""
class customerSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        customers = CUSTOMER.objects.filter(Q(name__istartswith=query) | Q(contact__istartswith=query)).order_by('pk')
        paginator = Paginator(customers, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'customers': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(self.request, 'customer_list', path="customer"), 'table', context)
        
        
        return HttpResponse(response)
    




"""
CUSTOMER UPDATE VIEW
"""
class customerUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, id):
        
        customer = get_object_or_404(CUSTOMER, pk=id)
        form = customerForm(instance=customer)
        context = {'form':form, 'heading':'Update Customer','isUpdate':True, 'object': customer}
        template_name = get_template(request, 'customer_add', path="customer")
        
        return render(request, template_name, context)
    
    def post(self, request, id):
        
        customer = get_object_or_404(CUSTOMER, pk=id)
        form = customerForm(instance=customer, data=request.POST, files=request.FILES)
        
        if form.is_valid():
            
            customer = form.save()
            messages.success(request, f'{customer} Update Successfully')
            return hx_Redirect("core:customerList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Customer','isUpdate':True, 'object': customer}
        template_name = get_template(request, 'customer_add', path="customer")
        
        return render(request,template_name, context)



"""
CUSTOMER DELETE VIEW
"""

class customerDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, id):
       
        try:
            
            customer = get_object_or_404(CUSTOMER, pk=id)
            
            context = {'object': customer, 'msg': f'Are you sure you want to delete  <strong> <i>{customer.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete', path="customer"), context)
        

        except Http404:
            
            return render(request, get_template(request, '404', path="customer")) 
    
    
    
    def post(self, request, id):
        
        customer = get_object_or_404(CUSTOMER, pk=id)
        customer.delete()
        messages.success(request, "Customer Deleted Successfully")
        return hx_Redirect("core:customerList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete', path="customer"), context)
    



"""
****************************************** Designation SECTION ******************************************
"""

"""
DESIGNATION CREATE VIEW
"""
class designationAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {'form': customerForm(),'heading':'Add Designation'}
        template = get_template(request, 'add', path="designation")
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = designationForm(data=request.POST)
        if form.is_valid():
            
            desig = form.save()
            form = designationForm()
            
            messages.success(request, "Designation Addedd Successfully")
            return hx_Redirect("core:designationList")
            
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'add', path="designation")
        
        context = {'form': form}
        return render(request,template, context)


"""
DESIGNATION LIST VIEW
"""
class designationListView(LoginRequiredMixin,ListView):
    
    model = DESIGNATION
    context_object_name = 'designations'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'list', path="designation")
    
    def get_queryset(self):
        return DESIGNATION.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(designationListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(designationListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context



"""
DESIGNATION UPDATE VIEW
"""
class designationUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, id):
        
        desig = get_object_or_404(DESIGNATION, pk=id)
        form = designationForm(instance=desig)
        context = {'form':form, 'heading':'Update Designation','isUpdate':True, 'object': desig}
        template_name = get_template(request, 'add', path="designation")
        
        return render(request, template_name, context)
    
    def post(self, request, id):
        
        desig = get_object_or_404(DESIGNATION, pk=id)
        form = designationForm(instance=desig, data=request.POST)
        
        if form.is_valid():
            
            desig = form.save()
            messages.success(request, f'{desig} Update Successfully')
            return hx_Redirect("core:designationList")
            
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Designation','isUpdate':True, 'object': desig}
        template_name = get_template(request, 'add', path="designation")
        
        return render(request,template_name, context)


"""
CUSTOMER DELETE VIEW
"""

class designationDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, id):
       
        try:
            
            desig = get_object_or_404(DESIGNATION, pk=id)
            
            context = {'object': desig, 'msg': f'Are you sure you want to delete  <strong> <i>{desig.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete', path="designation"), context)
        

        except Http404:
            
            return render(request, get_template(request, '404', path="designation")) 
    
    
    
    def post(self, request, id):
        
        desig = get_object_or_404(DESIGNATION, pk=id)
        desig.delete()
        messages.success(request, "Designation Deleted Successfully")
        return hx_Redirect("core:designationList")
        
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete', path="designation"), context)
    


"""
CUSTOMER SEARCH VIEW
"""
class designationSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        designations = DESIGNATION.objects.filter(name__istartswith=query).order_by('pk')
        paginator = Paginator(designations, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'designations': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(self.request, 'list', path="designation"), 'table', context)
        
        
        return HttpResponse(response)
  