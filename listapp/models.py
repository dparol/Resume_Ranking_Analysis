from django.db import models

# Create your models here.

class ResumeManager(models.Model):

    resume=models.FileField(upload_to='resumes/',null=True,blank=True)
    key_skill=models.CharField(max_length=200)
    emp_name=models.CharField(max_length=100)
    emp_email=models.EmailField()

