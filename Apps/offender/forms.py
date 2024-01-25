from django import forms
from .models import Offender
from crispy_forms.helper import FormHelper

class offenderForm(forms.ModelForm):
    

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
    
    class Meta:
        model = Offender
        fields = '__all__'
        
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'})
        }
    
  
    