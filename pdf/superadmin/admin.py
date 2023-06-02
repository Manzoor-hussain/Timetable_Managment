from django.contrib import admin


from .models import Constraint, Allstudent ,Allcourse

admin.site.register(Constraint)
admin.site.register(Allstudent)
admin.site.register(Allcourse)

# Register your models here.
