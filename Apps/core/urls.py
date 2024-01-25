from django.urls import path
from . import views
app_name = "core"

urlpatterns = [
    
    path('area/list/', views.areaListView.as_view(), name="areaList"),
    path('area/add/', views.areaAddView.as_view(), name="areaAdd"),
    path('area/search/', views.areaSearchView.as_view(), name="areaSearch"),
    path('area/update/<slug:slug>/', views.areaUpdateView.as_view(), name="areaUpdate"),
    path('area/delete/<slug:slug>/', views.areaDeleteView.as_view(), name="areaDelete"),
    
    
    # TREE SPECIE PATHS
    
    path('specie/list/', views.specieListView.as_view(), name="specieList"),
    path('specie/add/', views.specieAddView.as_view(), name="specieAdd"),
    path('specie/search/', views.specieSearchView.as_view(), name="specieSearch"),
    path('specie/update/<slug:slug>/', views.specieUpdateView.as_view(), name="specieUpdate"),
    path('specie/delete/<slug:slug>/', views.specieDeleteView.as_view(), name="specieDelete"),
    
    
     # CUSTOMER PATHS
     
    path('customer/list/', views.customerListView.as_view(), name="customerList"),
    path('customer/add/', views.customerAddView.as_view(), name="customerAdd"),
    path('customer/search/', views.customerSearchView.as_view(), name="customerSearch"),
    path('customer/update/<int:id>/', views.customerUpdateView.as_view(), name="customerUpdate"),
    path('customer/delete/<int:id>/', views.customerDeleteView.as_view(), name="customerDelete"),


      # CUSTOMER PATHS
     
    path('designation/list/', views.designationListView.as_view(), name="designationList"),
    path('designation/add/', views.designationAddView.as_view(), name="designationAdd"),
    path('designation/search/', views.designationSearchView.as_view(), name="designationSearch"),
    path('designation/update/<int:id>/', views.designationUpdateView.as_view(), name="designationUpdate"),
    path('designation/delete/<int:id>/', views.designationDeleteView.as_view(), name="designationDelete"),
]
