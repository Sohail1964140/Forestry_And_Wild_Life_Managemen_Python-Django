from django import forms
from .models import IncomeSource, ExpenseSource, Income, Expense
from crispy_forms.helper import FormHelper

class IncomeSourceForm(forms.ModelForm):
    """
    INCOME SOURCE FORM
    """
    class Meta:
        
        model = IncomeSource
        fields = '__all__'
        exclude = ['slug']

    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class IncomeForm(forms.ModelForm):
    """
    INCOME  FORM
    """
    class Meta:
        
        model = Income
        fields = '__all__'
    
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        

class ExpenseForm(forms.ModelForm):
    """
    EXPENSE  FORM
    """
    class Meta:
        
        model = Expense
        fields = '__all__'
        
        widgets = {'date': forms.DateInput(attrs={'type':'date'})}
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        
        
        

class ExpenseSourceForm(forms.ModelForm):
    """
    EXPENSE SOURCE FORM
    """
    class Meta:
        
        model = ExpenseSource
        fields = '__all__'
        exclude = ['slug']
    
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False