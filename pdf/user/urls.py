from django.contrib import admin
from django.urls import path, include
from .views import *


'''
    This is url file here three url 
    one for dashboard and another one select courses
    third for view your timetable.
 
 '''
urlpatterns = [
     path('dashboard/', get_index_page, name='dashboard'), 
     path('select-courses/', select_courses, name='select_courses'),
     path('show-timetable/', show_timetable, name='show_timetable'),     
]
