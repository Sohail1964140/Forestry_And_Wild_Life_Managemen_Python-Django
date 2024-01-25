from django.urls import path
from . import views
app_name="employee"

urlpatterns = [
    
    path("add/", views.empAddView.as_view(), name="empAdd"),
    path("list/", views.empListView.as_view(), name="empList"),
    path("search/", views.empSearchView.as_view(), name="empSearch"),
    path("update/<int:pk>/", views.empUpdateView.as_view(), name="empUpdate"),
    path("delete/<int:pk>/", views.empDeleteView.as_view(), name="empDelete"),
    
    
    # Visits
    path("visit/add/", views.visitAddView.as_view(), name="visitAdd"),
    path("visit/list/", views.visitListView.as_view(), name="visitList"),
    path("visit/update/<int:pk>", views.visitUpdateView.as_view(), name="visitUpdate"),
    path("visit/delete/<int:pk>", views.visitDeleteView.as_view(), name="visitDelete"),
    
    
]
