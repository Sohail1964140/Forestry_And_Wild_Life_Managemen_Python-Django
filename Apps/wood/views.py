from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse
from .forms import woodEntryForm, treeAltmentForm, woodAuctionForm
from .models import WoodAuction, WoodEntry, TreeAltment
from Apps.core.models import ForestArea
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
from django.views.generic import CreateView
from datetime import datetime
from Apps.core.models import CUSTOMER
from Apps.core.views import hx_Redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def get_template(request, name, path="woodEntry"):
    
    if request.htmx:
        return f'{path}/partials/{name}.html'
    
    return f'{path}/{name}.html'


class woodAddView(LoginRequiredMixin,View):
        
    """
    WOOD CREATE VIEW
    """
    
    def get(self, request):
        
        
        context = {'form': woodEntryForm(),'heading':'Add Wood'}
        template = get_template(request, 'wood_add')
        
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = woodEntryForm(data=request.POST)
        if form.is_valid():
            
            form.save()
            form = woodEntryForm()
            
            messages.success(request, "Data Addedd Successfully")
            return hx_Redirect("wood:woodEntryList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'wood_add')
        
        context = {'form': form}
        return render(request,template, context)

class woodListView(LoginRequiredMixin,ListView):
    
    """
    WOOD  LIST VIEW
    """
    model = WoodEntry
    context_object_name = 'woods'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'wood_list')
    
    def get_queryset(self):
        return WoodEntry.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(woodListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(woodListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context["areas"] = ForestArea.objects.all()
        return context

class woodSearchView(LoginRequiredMixin,View):
    """
    WOOD  SEARCHE VIEW
    """
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = 1
        
        woods = WoodEntry.objects.filter(Q(area__pk=query)).order_by('pk')
        paginator = Paginator(woods, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'woods': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'reas': ForestArea.objects.all()
        }
        
        response = render_block_to_string(get_template(request,'wood_list'), 'table', context)
        
        
        return HttpResponse(response)
    
class woodUpdateView(LoginRequiredMixin,View):
    """
    WOOD UPDATE VIEW
    """

    def get(self, request, id):
        
        wood = get_object_or_404(WoodEntry, pk=id)
        form = woodEntryForm(instance=wood)
        context = {'form':form, 'heading':'Update Wood','isUpdate':True, 'object': wood}
        template_name =  get_template(request, 'wood_add')
        
        return render(request, template_name, context)
    
    def post(self, request, id):
        
        wood = get_object_or_404(WoodEntry, pk=id)
        form = woodEntryForm(instance=wood, data=request.POST)
        
        if form.is_valid():
            
            wood = form.save()
            messages.success(request, f'Updated Successfully')
            return hx_Redirect("wood:woodEntryList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Income','isUpdate':True, 'object': wood}
        template_name =  get_template(request, 'wood_add')
        
        return render(request,template_name, context)

class woodDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, id):
       
        try:
            
            wood = get_object_or_404(WoodEntry, pk=id)
            
            context = {'object': wood, 'msg': f'Are you sure you want to delete  <strong> <i>{wood}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete'), context)
        

        except Http404:
            
            return render(request, get_template(request, '404')) 
    
    
    
    def post(self, request, id):
        
        wood = get_object_or_404(WoodEntry, pk=id)
        wood.delete()
        messages.success(request, "Wood Deleted Successfully")
        return hx_Redirect("wood:woodEntryList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete'), context)
    

# Auction views


class auctionAddView(LoginRequiredMixin,View):
        
    def get(self, request):
        
        
        context = {'form': woodAuctionForm(),'heading':'Add Auction'}
        template = get_template(request, 'auction_add', path="woodAuction")
        
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = woodAuctionForm(data=request.POST)
        if form.is_valid():
            
            form.save()
            form = woodAuctionForm()
            
            messages.success(request, "Data Addedd Successfully")
            return hx_Redirect("wood:auctionList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'auction_add', path="woodAuction")
        
        context = {'form': form}
        return render(request,template, context)



class auctionListView(LoginRequiredMixin,ListView):
    
    
    model = WoodAuction
    context_object_name = 'auctions'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'auction_list', path="woodAuction")
    
    def get_queryset(self):
        return WoodAuction.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(auctionListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(auctionListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        
        return context


class auctionUpdateView(LoginRequiredMixin,View):
   

    def get(self, request, id):
        
        auction = get_object_or_404(WoodAuction, pk=id)
        form = woodAuctionForm(instance=auction)
        
        context = {'form':form, 'heading':'Update Auction','isUpdate':True, 'object': auction}
        template = get_template(request, 'auction_add', path="woodAuction")
        
        return render(request, template, context)
    
    def post(self, request, id):
        
        auction = get_object_or_404(WoodAuction, pk=id)
        form = woodAuctionForm(instance=auction, data=request.POST)
        
        if form.is_valid():
            
            auction = form.save()
            messages.success(request, f'Updated Successfully')
            return hx_Redirect("wood:auctionList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Auction','isUpdate':True, 'object': auction}
        template = get_template(request, 'auction_add', path="woodAuction")
        
        return render(request,template, context)


class auctionDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, id):
       
        try:
            
            auction = get_object_or_404(WoodAuction, pk=id)
            
            context = {'object': auction, 'msg': f'Are you sure you want to delete  <strong> <i>{auction}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete',path="woodAuction"), context)
        

        except Http404:
            
            return render(request, get_template(request, '404', path="woodAuction")) 
    
    
    
    def post(self, request, id):
        
        auction = get_object_or_404(WoodAuction, pk=id)
        auction.delete()
        messages.success(request, "Auction Deleted Successfully")
        return hx_Redirect("wood:auctionList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete', path="woodAuction"), context)




class auctionSearchView(LoginRequiredMixin,View):
   
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('date')
        
        
        if query is None or '':
            date = datetime.now()
        else:
            date = datetime.strptime(query,'%Y-%m-%d')
        
        auctions = WoodAuction.objects.filter(Q(date__year=date.year)).order_by('pk')
        paginator = Paginator(auctions, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'auctions': page.object_list,
            'page_obj': page,
            'isSearch': True,
            
        }
        
        response = render_block_to_string(get_template(request,'auction_list',path="woodAuction"), 'table', context)
        
        
        return HttpResponse(response)

# Tree Alatment views

class treeAlatmentAddView(LoginRequiredMixin,View):
        
    def get(self, request):
        
        
        context = {'form': treeAltmentForm(),'heading':'Add Tree Alatment'}
        template = get_template(request, 'add', path="treeAltment")
        
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        
        form = treeAltmentForm(data=request.POST)
        if form.is_valid():
            
            form.save()
            form = treeAltmentForm()
            
            messages.success(request, "Data Addedd Successfully")
            return hx_Redirect("wood:alatmentList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'add', path="treeAltment")
        
        context = {'form': form}
        return render(request,template, context)



class treeAlatmentListView(LoginRequiredMixin,ListView):
    
    
    model = TreeAltment
    context_object_name = 'altms'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'list', path="treeAltment")
    
    def get_queryset(self):
        return TreeAltment.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(treeAlatmentListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(treeAlatmentListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context['customers'] = CUSTOMER.objects.all()
        context['areas'] =  ForestArea.objects.all()
        return context


class treeAlatmentUpdateView(LoginRequiredMixin,View):
   

    def get(self, request, id):
        
        alatment = get_object_or_404(TreeAltment, pk=id)
        form = treeAltmentForm(instance=alatment)
        
        context = {'form':form, 'heading':'Update Tree Alatments','isUpdate':True, 'object': alatment}
        template = get_template(request, 'add', path="treeAltment")
        
        return render(request, template, context)
    
    def post(self, request, id):
        
        alatment = get_object_or_404(TreeAltment, pk=id)
        form = treeAltmentForm(instance=alatment, data=request.POST)
        
        if form.is_valid():
            
            alatment = form.save()
            messages.success(request, f'Updated Successfully')
            return hx_Redirect("wood:alatmentList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Tree Alatments','isUpdate':True, 'object': alatment}
        template = get_template(request, 'add', path="treeAltment")
        
        return render(request,template, context)


class treeAlatmentDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, id):
       
        try:
            
            alatment = get_object_or_404(TreeAltment, pk=id)
            
            context = {'object': alatment, 'msg': f'Are you sure you want to delete  <strong> <i>{alatment}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete',path="treeAltment"), context)
        

        except Http404:
            
            return render(request, get_template(request, '404', path="treeAltment")) 
    
    
    
    def post(self, request, id):
        
        alatment = get_object_or_404(TreeAltment, pk=id)
        alatment.delete()
        messages.success(request, "Data Deleted Successfully")
        return hx_Redirect("wood:alatmentList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete', path="treeAltment"), context)


class treeAlatmentSearchView(LoginRequiredMixin,View):
   
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('customer')
        
        customer =  CUSTOMER.objects.filter(pk=query).first()
        
        
        if customer is None:
            
            altments = TreeAltment.objects.all().order_by("pk")
        else:
            altments = customer.altments.all().order_by("pk")
            
        paginator = Paginator(altments, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'altms': page.object_list,
            'page_obj': page,
            'isSearch': True,
            
        }
        
        response = render_block_to_string(get_template(request,'list',path="treeAltment"), 'table', context)
        
        
        return HttpResponse(response)
    



