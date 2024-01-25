from django.urls import path
from . import views as v

app_name = "incomeExpense"
urlpatterns = [
    
    # INCOME SOURCE PATHS
    
    path('income/source/list/', v.incomeSourceListView.as_view(), name="incomeSourceList"),
    path('income/source/add/', v.incomeSourceAddView.as_view(), name="incomeSourceAdd"),
    path('income/source/search/', v.incomeSourceSearchView.as_view(), name="incomeSourceSearch"),
    path('income/source/<slug:slug>/update/', v.incomeSourceUpdateView.as_view(), name="incomeSourceUpdate"),
    path('income/source/<slug:slug>/delete/', v.incomeSourceDeleteView.as_view(), name="incomeSourceDelete"),
    
    # INCOME  PATHS
    
    path('income/add/', v.incomeAddView.as_view(), name="incomeAdd"),
    path('income/list/', v.incomeListView.as_view(), name="incomeList"),
    path('income/search/', v.incomeSearchView.as_view(), name="incomeSearch"),
    path('income/<int:id>/update/', v.incomeUpdateView.as_view(), name="incomeUpdate"),
    path('income/<int:id>/delete/', v.incomeDeleteView.as_view(), name="incomeDelete"),
    
    # EXPENSE SOURCE PATHS
    
    path('expense/source/add/', v.expenseSourceAddView.as_view(), name="expenseSourceAdd"),
    path('expense/source/list/', v.expenseSourceListView.as_view(), name="expenseSourceList"),
    path('expense/source/search/', v.expenseSourceSearchView.as_view(), name="expenseSourceSearch"),
    path('expense/source/<slug:slug>/update/', v.expenseSourceUpdateView.as_view(), name="expenseSourceUpdate"),
    path('expense/source/<slug:slug>/delete/', v.expenseSourceDeleteView.as_view(), name="expenseSourceDelete"),
    
    
    
    # EXPENSE  PATHS
    path('expense/add/', v.expenseAddView.as_view(), name="expenseAdd"),
    path('expense/list/', v.expenseListView.as_view(), name="expenseList"),
    path('expense/search/', v.expenseSearchView.as_view(), name="expenseSearch"),
    path('expense/<int:id>/update/', v.expenseUpdateView.as_view(), name="expenseUpdate"),
    path('expense/<int:id>/delete/', v.expenseDeleteView.as_view(), name="expenseDelete"),
    
]
