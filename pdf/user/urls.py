from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
     path('dashboard/', get_index_page, name='dashboard'), 
     path('select-courses/', select_courses, name='select_courses'),
     path('show-timetable/', show_timetable, name='show_timetable'),
     
]
