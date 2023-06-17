from django.db import models 
from django.contrib.auth.models import User



'''
    This model for courses course time start and end time  
    and day name
   
 
 '''
class Allcourse(models.Model):
    DAYS_OF_WEEK = (
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
       
    )
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
    studentcount = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        return self.name
    

'''
    This model for Student which taking courses  
 '''
class Allstudent(models.Model):
    course = models.ForeignKey(Allcourse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title =models.CharField(max_length=200,null=True)
   

'''
    This model for Constraint which student can add at the 
    time of selecting courses 
 '''
class Constraint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name




    
  
    
  