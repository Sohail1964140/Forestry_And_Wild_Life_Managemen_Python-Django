from django import forms
from .models import ForestArea, TreeSpecies, CUSTOMER, DESIGNATION
from crispy_forms.helper import FormHelper

class forestAreaForm(forms.ModelForm):
    
    class Meta:
        model = ForestArea
        fields = '__all__'
        exclude = ['slug']
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class specieForm(forms.ModelForm):
    
    class Meta:
        model = TreeSpecies
        fields = '__all__'
        exclude = ['slug']
        
    def __init__(self, *args, **kwargs):
        
        super(specieForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class customerForm(forms.ModelForm):
      
    class Meta:
        model = CUSTOMER
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        
        super(customerForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class designationForm(forms.ModelForm):
    
    class Meta:
        model = DESIGNATION
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False