from django.urls import path
from . import views
urlpatterns = [
    
    path('add/', views.offenderAddView.as_view(), name="offenderAdd"),
    path('list/', views.offenderListView.as_view(), name="offenderList"),
    path('update/<int:pk>/', views.offenderUpdateView.as_view(), name="offenderUpdate"),
    path('delete/<int:pk>/', views.offenderDeleteView.as_view(), name="offenderDelete"),
    path('search/', views.offenderSearchView.as_view(), name="offenderSearch"),
    
]
