from django.urls import path
from . import views
urlpatterns = [
    
    path('add/',views.complaintAddView.as_view(), name="complaintAdd"),
    path('list/',views.complaintListView.as_view(), name="complaintList"),
    path('delete/<int:pk>',views.complaintDeleteView.as_view(), name="complaintDelete"),
    path('update/<int:pk>',views.complaintUpdateView.as_view(), name="complaintUpdate"),
    path('search', views.complaintSearchView.as_view(), name="complaintSearch"),
    path('partial/delete',views.deletePartial, name="partialDelete"),
    
    # video paths
    path('video/add',views.loadVideoFormView, name="videoAddForm"),
    path('video/delete/<int:pk>',views.deleteVideoEvidance, name="videoDelete"),
    
    # Image paths
    path('image/add',views.loadImageFormView, name="imageAddForm"),
    path('image/delete/<int:pk>',views.imageEvidanceDelete, name="imageDelete"),
    
    
]
