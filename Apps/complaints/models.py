from django.db import models
from django.contrib.auth import get_user_model
from Apps.core.models import ForestArea
# Create your models here.

STATUS_CHOICES = (
    ('0', 'Pending'),
    ('1', 'Acitve'),
    ('2', 'Complete'),
)

class Complaints(models.Model):
    
    subject = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.TextField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=0)
    employee = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    area = models.ForeignKey(to=ForestArea, on_delete=models.CASCADE)


    @property
    def getActiveComplaints(self)->int:

        return self.objects.filter(status=1).count()




class evidanceVideo(models.Model):
    
    complaint = models.ForeignKey(to=Complaints, on_delete=models.CASCADE,related_name="videos")
    video = models.FileField(upload_to="complaints/videos/")

class evidancImage(models.Model):
    
    complaint = models.ForeignKey(to=Complaints, on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="complaints/images/")