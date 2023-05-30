from django.contrib import admin

from .models import Service, Permission, Mypermission, Myservice, Countservices, Course, Timetable,Student, Allcourse
from .models import Constraint, Allstudent

admin.site.register(Constraint)
admin.site.register(Allstudent)
admin.site.register(Myservice)
admin.site.register(Mypermission)
admin.site.register(Countservices)
admin.site.register(Course)
admin.site.register(Timetable)
admin.site.register(Student)
admin.site.register(Allcourse)

# Register your models here.
