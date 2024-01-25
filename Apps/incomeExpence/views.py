from django.shortcuts import render,HttpResponse
from .forms import IncomeSourceForm, ExpenseSourceForm, IncomeForm, ExpenseForm
from .models import IncomeSource, ExpenseSource, Income, Expense
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
from Apps.core.views import hx_Redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def get_template(request, name, path):
    
    if request.htmx:
        return f'{path}/partials/{name}.html'
    
    return f'{path}/{name}.html'




"""
********************************************** INCOME SOURCE **********************************************
"""

class incomeSourceAddView(LoginRequiredMixin,View):
        
    """
    Income Source CREATE VIEW
    """
    
    def get(self, request):
        
        print("i am okay bro")
        context = {'form': IncomeSourceForm(),'heading':'Add Income Source'}
        template = get_template(request, 'source_add', path="incomesource")
        print("i am okay bro")
        
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = IncomeSourceForm(data=request.POST)
        if form.is_valid():
            
            form.save()
            form = IncomeSourceForm()
            
            messages.success(request, "Data Addedd Successfully")
            return hx_Redirect("incomeExpense:incomeSourceList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'source_add', path="incomesource")
        
        context = {'form': form}
        return render(request,template, context)
    
    

class incomeSourceListView(LoginRequiredMixin,ListView):
    
    """
    INCOME SOURCE LIST VIEW
    """
    model = IncomeSource
    context_object_name = 'sources'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'source_list', path="incomesource")
    
    def get_queryset(self):
        return IncomeSource.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(incomeSourceListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(incomeSourceListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context



class incomeSourceSearchView(LoginRequiredMixin,View):
    """
    INCOME SOURCE SEARCHE VIEW
    """
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        incomeSource = IncomeSource.objects.filter(Q(name__istartswith=query)).order_by('pk')
        paginator = Paginator(incomeSource, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'sources': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(request,'source_list', path="incomesource"), 'table', context)
        
        
        return HttpResponse(response)
    

class incomeSourceUpdateView(LoginRequiredMixin,View):
    """
    INCOME SOURCE UPDATE VIEW
    """

    def get(self, request, slug):
        
        incomesource = get_object_or_404(IncomeSource, slug=slug)
        form = IncomeSourceForm(instance=incomesource)
        context = {'form':form, 'heading':'Update Income Source','isUpdate':True, 'object': incomesource}
        template_name = get_template(request, 'source_add', path="incomesource")
        
        return render(request, template_name, context)
    
    def post(self, request, slug):
        
        incomesource = get_object_or_404(IncomeSource, slug=slug)
        form = IncomeSourceForm(instance=incomesource, data=request.POST)
        
        if form.is_valid():
            
            incomesource = form.save()
            messages.success(request, f'{incomesource} Update Successfully')
            return hx_Redirect("incomeExpense:incomeSourceList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Income Source','isUpdate':True, 'object': incomesource}
        template_name = get_template(request, 'source_add', path="incomesource")
        
        return render(request,template_name, context)




class incomeSourceDeleteView(LoginRequiredMixin,View):
    
    """
    INCOME SOURCE DELETE VIEW
    """
    def get(self, request, slug):
       
        try:
            
            incomesource = get_object_or_404(IncomeSource, slug=slug)
            
            context = {'object': incomesource, 'msg': f'Are you sure you want to delete  <strong> <i>{incomesource.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete', path="incomesource"), context)
        

        except Http404:
            
            
            return render(request, get_template(request, '404', path="incomesource")) 
    
    
    
    def post(self, request, slug):
        

        incomesource = get_object_or_404(IncomeSource, slug=slug)


        
        incomesource.delete()
        messages.success(request, f'{incomesource.name} deleted successfully')

        return hx_Redirect("incomeExpense:incomeSourceList")
        # context = {'isDeleted': True,'msg': f'{incomesource.name} deleted Successfully'}
        # return render(request, get_template(request, 'delete', path="incomesource"), context)





"""
********************************************** EXPENSE SOURCE **********************************************
"""



class expenseSourceAddView(LoginRequiredMixin,View):
        
    """
    EXPENSE SOURCE CREATE VIEW
    """
    
    def get(self, request):
        
        context = {'form': ExpenseSourceForm(),'heading':'Add Income Source'}
        template = get_template(request, 'source_add', path="expensesource")
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = ExpenseSourceForm(data=request.POST)
        if form.is_valid():
            
            form.save()
            form = ExpenseSourceForm()
            
            messages.success(request, "Data Addedd Successfully")
            return hx_Redirect("incomeExpense:expenseSourceList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'source_add', path="expensesource")
        
        context = {'form': form}
        return render(request,template, context)
    
    

class expenseSourceListView(LoginRequiredMixin,ListView):
    
    """
    EXPENSE SOURCE LIST VIEW
    """
    model = ExpenseSource
    context_object_name = 'sources'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'source_list', path="expensesource")
    
    def get_queryset(self):
        return ExpenseSource.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(expenseSourceListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(expenseSourceListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context



class expenseSourceSearchView(LoginRequiredMixin,View):
    """
    EXPENSE SOURCE SEARCHE VIEW
    """
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        expenseSource = ExpenseSource.objects.filter(Q(name__istartswith=query)).order_by('pk')
        paginator = Paginator(expenseSource, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'sources': page.object_list,
            'page_obj': page,
            'isSearch': True
        
        }
        
        response = render_block_to_string(get_template(request,'source_list', path="expensesource"), 'table', context)
        
        
        return HttpResponse(response)
    

class expenseSourceUpdateView(LoginRequiredMixin,View):
    """
    EXPENSE SOURCE UPDATE VIEW
    """

    def get(self, request, slug):
        
        expensesource = get_object_or_404(ExpenseSource, slug=slug)
        form = ExpenseSourceForm(instance=expensesource)
        context = {'form':form, 'heading':'Update Expense Source','isUpdate':True, 'object': expensesource}
        template_name = get_template(request, 'source_add', path="expensesource")
        
        return render(request, template_name, context)
    
    def post(self, request, slug):
        
        expensesource = get_object_or_404(ExpenseSource, slug=slug)
        form = ExpenseSourceForm(instance=expensesource, data=request.POST)
        
        if form.is_valid():
            
            expensesource = form.save()
            messages.success(request, f'{expensesource} Update Successfully')
            return hx_Redirect("incomeExpense:expenseSourceList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Expense Source','isUpdate':True, 'object': expensesource}
        template_name = get_template(request, 'source_add', path="expensesource")
        
        return render(request,template_name, context)




class expenseSourceDeleteView(LoginRequiredMixin,View):
    
    """
    EXPENSE SOURCE DELETE VIEW
    """
    def get(self, request, slug):
       
        try:
            
            expensesource = get_object_or_404(ExpenseSource, slug=slug)
            
            context = {'object': expensesource, 'msg': f'Are you sure you want to delete  <strong> <i>{expensesource.name}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete', path="expensesource"), context)
        

        except Http404:
            
            
            return render(request, get_template(request, '404', path="expensesource")) 
    
    
    
    def post(self, request, slug):
        
        
       
        expensesource = get_object_or_404(ExpenseSource, slug=slug)

        expensesource.delete()
        messages.success(request, f'{expensesource.name} deleted successfully')

        return hx_Redirect("incomeExpense:expenseSourceList")
        # context = {'isDeleted': True,'msg': f'{expensesource.name} deleted Successfully'}
        # return render(request, get_template(request, 'delete', path="expensesource"), context)




"""
********************************************** INCOME **********************************************
"""

class incomeAddView(LoginRequiredMixin,View):
        
    """
    Income CREATE VIEW
    """
    
    def get(self, request):
        
        
        context = {'form': IncomeForm(),'heading':'Add Income'}
        template = get_template(request, 'income_add', path="income")
        
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = IncomeForm(data=request.POST)
        if form.is_valid():
            
            form.save()
            form = IncomeForm()
            
            messages.success(request, "Data Addedd Successfully")
            return hx_Redirect("incomeExpense:incomeList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'income_add', path="income")
        
        context = {'form': form}
        return render(request,template, context)



class incomeListView(LoginRequiredMixin,ListView):
    
    """
    INCOME  LIST VIEW
    """
    model = Income
    context_object_name = 'incomes'
    paginate_by = 10
    paginate_orphans = 0
    
    def get_template_names(self): return get_template(self.request, 'income_list', path="income")
    
    def get_queryset(self):
        return Income.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(incomeListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(incomeListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context["sources"] = IncomeSource.objects.all()
        return context


class incomeSearchView(LoginRequiredMixin,View):
    """
    INCOME  SEARCHE VIEW
    """
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        income = Income.objects.filter(Q(source=query)).order_by('pk')
        paginator = Paginator(income, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'incomes': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'sources': IncomeSource.objects.all()
        }
        
        response = render_block_to_string(get_template(request,'income_list', path="income"), 'table', context)
        
        
        return HttpResponse(response)
    
class incomeUpdateView(LoginRequiredMixin,View):
    """
    INCOME UPDATE VIEW
    """

    def get(self, request, id):
        
        income = get_object_or_404(Income, pk=id)
        form = IncomeForm(instance=income)
        context = {'form':form, 'heading':'Update Income','isUpdate':True, 'object': income}
        template_name =  get_template(request, 'income_add', path="income")
        
        return render(request, template_name, context)
    
    def post(self, request, id):
        
        income = get_object_or_404(Income, pk=id)
        form = IncomeForm(instance=income,data=request.POST)
        
        if form.is_valid():
            
            income = form.save()
            messages.success(request, f'Updated Successfully')
            return hx_Redirect("incomeExpense:incomeList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Income','isUpdate':True, 'object': income}
        template_name =  get_template(request, 'income_add', path="income")
        
        return render(request,template_name, context)


"""
INCOME DELETE VIEW
"""

class incomeDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, id):
       
        try:
            
            income = get_object_or_404(Income, pk=id)
            
            context = {'object': income, 'msg': f'Are you sure you want to delete  <strong> <i>{income}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete', path="income"), context)
        

        except Http404:
            
            return render(request, get_template(request, '404', path="income")) 
    
    
    
    def post(self, request, id):
        
        income = get_object_or_404(Income, pk=id)
        income.delete()
        messages.success(request, "Income Deleted Successfully")
        return hx_Redirect("incomeExpense:incomeList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete', path="income"), context)
    
    
    
    
    """
********************************************** EXPENSE **********************************************
"""

class expenseAddView(LoginRequiredMixin,View):
        
    """
    EXPENSE CREATE VIEW
    """
    
    def get(self, request):
        
        
        context = {'form': ExpenseForm(),'heading':'Add Expense'}
        template = get_template(request, 'expense_add', path="expense")
        
        return render(request,template, context )
    
    
    def post(self, request):
        
        
        form = ExpenseForm(data=request.POST)
        if form.is_valid():
            
            form.save()
            form = ExpenseForm()
            
            messages.success(request, "Data Addedd Successfully")
            return hx_Redirect("incomeExpense:expenseList")
        else:
            messages.error(request, "Please Correct the error bellow")
        
        template = get_template(request, 'expense_add', path="expense")
        
        context = {'form': form}
        return render(request,template, context)



class expenseListView(LoginRequiredMixin,ListView):
    
    """
    EXPENSE  LIST VIEW
    """
    model = Expense
    context_object_name = 'expenses'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, 'expense_list', path="expense")
    
    def get_queryset(self):
        return Expense.objects.all().order_by('pk')
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(expenseListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(expenseListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context["sources"] = ExpenseSource.objects.all()
        return context


class expenseSearchView(LoginRequiredMixin,View):
    """
    EXPENSE  SEARCHE VIEW
    """
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        if query is None:
            query = ""
        
        expenses = Expense.objects.filter(Q(source=query)).order_by('pk')
        paginator = Paginator(expenses, per_page=10)
        
        
        
        page = paginator.get_page(page_number)
        
        context={
            
            'expenses': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'sources': ExpenseSource.objects.all()
        }
        
        response = render_block_to_string(get_template(request,'expense_list', path="expense"), 'table', context)
        
        
        return HttpResponse(response)
    
class expenseUpdateView(LoginRequiredMixin,View):
    """
    EXPENSE UPDATE VIEW
    """

    def get(self, request, id):
        
        expense = get_object_or_404(Expense, pk=id)
        form = ExpenseForm(instance=expense)
        context = {'form':form, 'heading':'Update Expense','isUpdate':True, 'object': expense}
        template_name =  get_template(request, 'expense_add', path="expense")
        
        return render(request, template_name, context)
    
    def post(self, request, id):
        
        expense = get_object_or_404(Expense, pk=id)
        form = ExpenseForm(instance=expense, data=request.POST)
        
        if form.is_valid():
            
            expense = form.save()
            messages.success(request, f'Updated Successfully')
            return hx_Redirect("incomeExpense:expenseList")
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        context = {'form':form, 'heading':'Update Expense','isUpdate':True, 'object': expense}
        template_name =  get_template(request, 'expense_add', path="expense")
        
        return render(request,template_name, context)


"""
EXPENSE DELETE VIEW
"""

class expenseDeleteView(LoginRequiredMixin,View):
    
    def get(self, request, id):
       
        try:
            
            expense = get_object_or_404(Expense, pk=id)
            
            context = {'object': expense, 'msg': f'Are you sure you want to delete  <strong> <i>{expense}</i></strong>? This action cannot be undone.'}
            
            return render(request,get_template(request, 'delete', path="expense"), context)
        

        except Http404:
            
            return render(request, get_template(request, '404', path="expense")) 
    
    
    
    def post(self, request, id):
        
        expense = get_object_or_404(Expense, pk=id)
        expense.delete()
        messages.success(request, "Expense Deleted Successfully")
        return hx_Redirect("incomeExpense:expenseList")
        # context = {
        #     'isDeleted':True
        # }
        # return render(request, get_template(request, 'delete', path="expense"), context)