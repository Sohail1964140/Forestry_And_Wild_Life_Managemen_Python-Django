from django import forms
from .models import Complaints, evidanceVideo, evidancImage
from django.core.exceptions import ValidationError
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model

class complaintsForm(forms.ModelForm):
    
        
    def __init__(self, *args, **kwargs):
        

        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        


    
    class Meta:
        
        model = Complaints
        fields = '__all__'
        exclude = ['employee']

VALID_VIDEO_EXTENTIONS = ['mp4', 'mov', 'avi']
def validateVideoFile(value):
    
    fileExtention = value.name.split('.')[-1].lower()
    
    if fileExtention not in VALID_VIDEO_EXTENTIONS:
        
        raise ValidationError("please select a video file")
    
    return value
    

class evidanceVideoForm(forms.ModelForm):
    # video = forms.FileField(validators=[validateVideoFile], widget=forms.FileInput())
    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['video'].widget.attrs = {'accept':'video/*'}
    class Meta:
        
        model = evidanceVideo
        fields = ['video']
    


VALID_IMAGE_EXTENTIONS = ['jpeg', 'jpg']
def validateImageFile(value):
    
    fileExtention = value.name.split('.')[-1].lower()
    
    if fileExtention not in VALID_IMAGE_EXTENTIONS:
        
        raise ValidationError("please select a image file")
    
    return value

class evidancImageForm(forms.ModelForm):
    image = forms.ImageField(validators=[validateImageFile])
            
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
    class Meta:
        
        model = evidancImage
        fields = ['image']