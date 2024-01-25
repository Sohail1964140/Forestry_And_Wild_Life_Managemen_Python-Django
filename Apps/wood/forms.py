from django import forms
from .models import WoodEntry, WoodAuction, TreeAltment
from crispy_forms.helper import FormHelper



class woodEntryForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        
    class Meta:
        
        model = WoodEntry
        fields = '__all__'
        

class woodAuctionForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["date"].widget = forms.DateInput(attrs={"type":"date"})
        
    class Meta:
        
        model = WoodAuction
        fields = '__all__'


class treeAltmentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["date"].widget = forms.DateInput(attrs={"type":"date"})
        
    class Meta:
        
        model = TreeAltment
        fields = '__all__'
