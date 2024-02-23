from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('uploadresume',views.upload_resume,name='upload_resume'),
]