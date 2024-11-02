from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('create-resume/', views.create_resume, name='create-resume'),
    path('resume/<int:resume_id>/', views.resume, name='resume'),
    path('resume_pdf/<int:resume_id>/', views.resume_pdf, name='resume_pdf'),
]
