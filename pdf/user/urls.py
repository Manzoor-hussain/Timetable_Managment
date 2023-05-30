from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
  
     #path('index/', index, name='index'),
     path('dashboard/', get_index_page, name='dashboard'),
     path('upload_file/', upload_file, name='upload_file'),
     path('upload_file/<str:service>/', upload_file, name='upload_file'),
     path('select-courses/', perform_services, name='perform_services'),
     path('show-timetable/', show_timetable, name='show_timetable'),
     
     path('download_docx/', download_docx, name='download_docx'),

     
]
