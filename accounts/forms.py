from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper

class UserForm(UserCreationForm):
   
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        
        for field in self.fields.values():
            field.help_text  = ""
        
        self.fields['password1'].widget.attrs  ={'class': 'form-class pass-input'} 
        self.fields['password2'].widget.attrs  ={'class': 'form-class pass-input'} 
        
        
    class Meta:
        model = get_user_model()
        
        fields = [
            'employee','email','username','password1','password2', 
        ]
        