from django.db import models 
from django.contrib.auth.models import User


# Create your models here.
class Service(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    is_permisstion = models.BooleanField(default=False)

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_check = models.BooleanField(default=True)
class Myservice(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    is_permisstion = models.BooleanField(default=False)
class Mypermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Myservice, on_delete=models.CASCADE)
    is_check = models.BooleanField(default=True)
class Countservices(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    service=models.ForeignKey(Myservice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField()


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Timetable(models.Model):
    DAYS_OF_WEEK = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=100)
    constraint = models.CharField(max_length=200, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
class Allcourse(models.Model):
    DAYS_OF_WEEK = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
    studentcount = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        return self.name
class Allstudent(models.Model):
    course = models.ForeignKey(Allcourse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title =models.CharField(max_length=200,null=True)
   


class Constraint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name




    
  
    
  