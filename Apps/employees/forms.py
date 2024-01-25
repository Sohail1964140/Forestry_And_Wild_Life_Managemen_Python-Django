from django import forms


from .models import EMPLOYEE, VISIT
from crispy_forms.helper import FormHelper

class empForm(forms.ModelForm):
    
    class Meta:
        model = EMPLOYEE
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        self.fields['contact'].widget = forms.TextInput(attrs={'id':'phone', "maxlength":"11"})
        self.fields['email'].widget = forms.EmailInput(attrs={'id':'email', "maxlength":"30"})
        
        
        
"""
-<( === === === === === === === === === === === === VISIT  === === === === === === === === === === === === )>-
"""
class visitForm(forms.ModelForm):
    
    class Meta:
        model = VISIT
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['date'].widget = forms.DateInput(attrs={'type':'date'})
        self.fields['employees'] = forms.ModelMultipleChoiceField(queryset=EMPLOYEE.objects.all(),widget=forms.CheckboxSelectMultiple)