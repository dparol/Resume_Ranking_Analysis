from django.db import models

# Create your models here.

class ResumeManager(models.Model):

    resume=models.FileField(upload_to='resumes/',null=True,blank=True)
    key_skill=models.CharField(max_length=200)
    candidate_name=models.CharField(max_length=100,null=True,blank=True)
    candidate_email=models.EmailField(null=True,blank=True)
    candidate_contactNumber=models.CharField(max_length=50,null=True,blank=True)
    candidate_education=models.CharField(max_length=200,null=True,blank=True)
    
    
    


