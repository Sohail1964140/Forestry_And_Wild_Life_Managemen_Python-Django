from django.shortcuts import render,HttpResponse
from .forms import complaintsForm, evidanceVideoForm, evidancImageForm
from .models import Complaints, evidanceVideo, evidancImage
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
from Apps.core.models import ForestArea
from Apps.core.views import hx_Redirect
from Apps.employees.models import EMPLOYEE
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

def get_template(request, name, path="complaints"):
    
    if request.htmx:
        return f'{path}/partials/{name}.html'
    
    return f'{path}/{name}.html'

def deletePartial(request):
    return HttpResponse("")



"""
COMPLAINT CREATE VIEW
"""
class complaintAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        
        context = {
            'compForm': complaintsForm(),
            'videoForm': evidanceVideoForm(),
            'imageForm': evidancImageForm(),
            'heading':'Add Complaint',
            
        }
        
        template = get_template(request ,name='complaint_add')
        return render(request,template, context )
    
    
    def post(self, request):
        
        compForm = complaintsForm(data=request.POST)
        
        if compForm.is_valid():
            complaint = compForm.save(commit=False)
            complaint.employee = request.user
            complaint.save()
            # compForm = complaintsForm()
            messages.success(request, "Complaint Addedd Successfully")
            request.session['complaint'] = complaint.pk
            
            return hx_Redirect("complaintList")
        else:
            messages.error(request, "Please  Correct the error bellow")
            
        template = get_template(request ,name='complaint_add')
        
        context = {
            'compForm': compForm,
            'videoForm': evidanceVideoForm(),
            'imageForm': evidancImageForm(),
            'heading':'Add Complaint',
            'isSubmit': True,
            'object': complaint,
            'isUpdate':True,
        }
        return render(request,template, context)




"""
COMPLAINT LIST VIEW
"""
class complaintListView(LoginRequiredMixin,ListView):
    
    model = Complaints
    context_object_name = 'complaints'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'complaint_list')
    
    def get_queryset(self):
        return Complaints.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(complaintListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(complaintListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context['areas'] = ForestArea.objects.all()
        context['employees'] = get_user_model().objects.all()
        return context
"""
COMPLAINT UPDATE VIEW
"""
class complaintUpdateView(LoginRequiredMixin,View):
    
        

    def get(self, request, pk):
        
        complaint = get_object_or_404(Complaints, pk=pk)
        form = complaintsForm(instance=complaint)
        
        videos = complaint.videos.all()
        images = complaint.images.all()
        
        request.session['complaint'] = complaint.pk
        
        context = {
            
            'compForm':form, 
            'heading':'Update Complaint',       
            'isUpdate':True, 
            'object': complaint,
            'images': images,
            'videos': videos,
            'isList':True,
            'isSubmit': True
            }
        
        template_name = get_template(request, 'complaint_add')
        
        return render(request, template_name, context)
    
    def post(self, request, pk):
        
        complaint = get_object_or_404(Complaints, pk=pk)
        form = complaintsForm(instance=complaint, data=request.POST)
        videos = complaint.videos.all()
        images = complaint.images.all()
        if form.is_valid():
            
            complaint = form.save()
            messages.success(request, f'{complaint} Update Successfully')
            return hx_Redirect("complaintList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {
            'compForm':form,
            'heading':'Update Complaint',
            'isUpdate':True,
            'object': complaint,
            'images': images,
            'videos': videos,
            'isList':True,
            'isSubmit': True
                   }
        template_name = get_template(request, 'complaint_add')
        
        return render(request,template_name, context)


"""
COMPLAINT SEARCH VIEW
"""
class complaintSearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = 1
        
        
        complaints = Complaints.objects.filter(Q(area__pk=query)).order_by('pk')
        
        paginator = Paginator(complaints, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'complaints': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(request,'complaint_list'), 'table', context)
        
        
        return HttpResponse(response)

"""
COMPLAINT DELETE VIEW
"""

class complaintDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, pk):
       
        try:
            
            complaint = get_object_or_404(Complaints, pk=pk)
            
            context = {'object': complaint, 'msg': f'Are you sure you want to delete  <strong> <i>{complaint}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete'), context)
        

        except Http404:
            
            return render(request, get_template(request, '404')) 
    
    
    
    def post(self, request, pk):
        
        complaint = get_object_or_404(Complaints, pk=pk)
        complaint.delete()
        messages.success(request, "Complaint Deleted Successfully")
        return hx_Redirect("complaintList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete'), context)


def loadImageFormView(request):
    imageForm = evidancImageForm()
    if request.method == "POST":
        
        imageForm = evidancImageForm(data=request.POST,files=request.FILES)
        
        if imageForm.is_valid():
            
            image = imageForm.save(commit=False)
            complaint = Complaints.objects.get(pk= request.session['complaint'])
            image.complaint = complaint
            image.save()
            
            return render(request, 'complaints/partials/imageForm.html',{'image': image, 'isList': True})
    
    context = {
        'imageForm': imageForm
    }
    return render(request, "complaints/partials/imageForm.html", context)




def loadVideoFormView(request):
    videoForm = evidanceVideoForm()
    if request.method == "POST":
        
        videoForm = evidanceVideoForm(data=request.POST,files=request.FILES)
        
        if videoForm.is_valid():
            
            video = videoForm.save(commit=False)
            complaint = Complaints.objects.get(pk= request.session['complaint'])
            video.complaint = complaint
            video.save()
            
            return render(request, 'complaints/partials/videoForm.html',{'video': video, 'isList': True})
    
    context = {
        'videoForm': videoForm
    }
    return render(request, "complaints/partials/videoForm.html", context)


def deleteVideoEvidance(request, pk):
    
    obj = evidanceVideo.objects.get(pk=pk)
    obj.delete()
    return HttpResponse("")


def imageEvidanceDelete(request, pk):
    
    obj = evidancImage.objects.get(pk=pk)
    obj.delete()
    return HttpResponse("")