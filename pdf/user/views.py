from django.http import Http404, HttpResponse
from django.shortcuts import render ,redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import  UserSerializerForTimeTable
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required

from django.db.models.functions import ExtractWeekDay
from django.db.models import Func
import datetime
from django.contrib.auth.models import User
from superadmin.models import  Allcourse, Allstudent, Constraint
import os
from  datetime import time
from itertools import groupby
from operator import itemgetter
from collections import OrderedDict
from datetime import datetime, time
import pdb

# Create your views here.
'''
    This function take three argument 
    request course for course object and constraint object 
   
    check_already_constraint
 
'''
def check_already_constraint(request,cours,constraint_obj):

    
    if cours:
        #orted_time_slots = sorted(course_list, key=lambda slot: slot['start_time'])

        if len(constraint_obj) >=2:
            print("list",constraint_obj)
            course_list = list(constraint_obj)
            time_differences = []
           
            first=constraint_obj.first()
            last = constraint_obj.last()
            if cours.start_time >=last.end_time:
                return True
            elif cours.end_time<=first.start_time:
                return True
                


            for constraint1, constraint2 in zip(course_list, course_list[1:]):   
                   
                    if constraint1.end_time <= cours.start_time <= constraint2.start_time and  constraint1.end_time <= cours.end_time <= constraint2.start_time:
                        return True
                      
                    # elif constraint1.start_time >= cours.end_time <= constraint1.end_time:
                    #     return True
                    
                    # elif len(constraint_obj) ==2:
                    #     if constraint2.end_time <= cours.start_time >= constraint2.start_time:
                    #         return True

                    
                    

            
            return False      

        elif len(constraint_obj) == 1:
            for const in constraint_obj:
               
                if const.start_time <= cours.start_time <= const.end_time or const.start_time <= cours.end_time <= const.end_time:
                    return False
                else:
                    return True
  
   

'''
    This function take five argument  and check one constraint with
    already existing constraint and courses.if any available slot for 
    constraint then constraint object is created. 
 
'''
def check_constraint_to_add(request,name,day,start_time,end_time):
    days = day[:3]
  
   
    constraint_obj=Constraint.objects.filter(user=request.user,day=day)
    allstudent=Allstudent.objects.filter(user=request.user) 
    student = Allcourse.objects.filter(allstudent__user=request.user,day=days)
    student_list=list(student)
    cons_list =list(constraint_obj)
    appended_list = student_list + cons_list
    sorted_list = sorted(appended_list, key=lambda x: x.start_time)
    first=sorted_list[0]
    last=sorted_list[len(sorted_list)-1]
    start_timee_2 = time.fromisoformat(start_time)
    end_timee_2 = time.fromisoformat(end_time)
    if start_timee_2 >=last.end_time:
        already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
        if already_cons:
            return False
        else:
            Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
            return True
    elif end_timee_2<=first.start_time:
        already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
        if already_cons:
            return False
        else:
            Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
            return True
    
    for constraint1, constraint2 in zip(sorted_list, sorted_list[1:]):   
            
            if constraint1.end_time <= start_timee_2 <= constraint2.start_time and  constraint1.end_time <= end_timee_2 <= constraint2.start_time:
                return True
                
 
    return False

    
    # start_timee_2 = time.fromisoformat(start_time)
    # end_timee_2 = time.fromisoformat(end_time)

    # if constraint_obj:
       
    #     for const in constraint_obj:
          
          
    #         if const.start_time <= start_timee_2 <= const.end_time or const.start_time <= end_timee_2 <= const.end_time:
    #             print("contine")
    #             continue
    #         else:
    #             print("else")
    #             allstudent=Allstudent.objects.filter(user=request.user) 
    #             student = Allcourse.objects.filter(allstudent__user=request.user,day=days)
    #             if student:
    #                 for stu in student:
    #                     if stu.start_time <= start_timee_2 <=stu.end_time or  stu.start_time <= end_timee_2 <=stu.end_time:
    #                         continue
    #                     else:
    #                         already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                         if already_cons:
    #                             continue
    #                         else:
    #                             myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                         break
    #             else:
    #                 already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                 if already_cons:
    #                     continue
    #                 else:
    #                     myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                 break
    # else:
        
    #     allstudent=Allstudent.objects.filter(user=request.user) 
    #     student = Allcourse.objects.filter(allstudent__user=request.user,day=days)
      
    #     if student:
    #         if len(student) == 1:

    #             for stu in student:
    #                 if stu.start_time <= start_timee_2 <=stu.end_time or  stu.start_time <= end_timee_2 <=stu.end_time:
    #                     continue
    #                 else:
    #                     already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                     if already_cons:
    #                         continue
    #                     else:
    #                         myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                     break
            
    #         elif len(student) >= 2:
    #            # res=check_for_day(request,course_,check,0)

            
    #             course_list = list(student)
                
    #             for cours in student:

    #                 time_differences = []
    #                 for course1, course2 in zip(course_list, course_list[1:]):
                        
    #                     if course1.end_time <= start_timee_2 < course2.start_time and  course1.end_time <= end_timee_2 <= course2.start_time:
                           
    #                         already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                         if already_cons:
    #                             continue
    #                         else:
    #                             myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                         break
    #                     elif course1.end_time <= start_timee_2 >= course2.end_time or course2.end_time <= start_timee_2 >= course1.end_time:
    #                         already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                         if already_cons:
    #                             continue
    #                         else:
    #                             myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #                         break
                           
                            
                                
                
    #     else:

    #         already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
    #         if already_cons:
    #             pass
    #         else:
    #             myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
           
            



                



'''
    This function take four  argument  and check the 
    student taking course with already existing courses
    and  constraint and given constraint.
 
'''

def check_for_day(request,course_,check,dday):
   
    day = request.POST.get('day')
    day_2 = request.POST.get('day_2')
  
    start_time_ = request.POST['start_time']
    end_time_ = request.POST['end_time']
    constraint_ = request.POST['constraint']
    days=day.upper()
    days_=days[:3]
   
    start_time_2 = request.POST['start_time_2']
    end_time_2 = request.POST['end_time_2']
    constraint_2 = request.POST['constraint_2']
    days_22=day_2.upper()
    days_2=days_22[:3]
   
   
    message =''
    for cours in course_:
       
        already_obj = Allstudent.objects.filter(user=request.user,title=check)
        allstudent=Allstudent.objects.filter(user=request.user) 
        timetable = Allcourse.objects.filter(allstudent__user=request.user,day=cours.day)
        days_2 = {"MON":"MONDAY", "TUE":'TUESDAY', "WED":"WEDNESDAY", "THU":'THURSDAY', "FRI":'FRIDAY',"SUN":'SUNDAY'}
        full_day=''
       
      
        if cours.day in days_2:
            full_day = days_2[cours.day]
       
       
        if not timetable:
            
            if already_obj:
                continue
            else:
                constraint_obj=Constraint.objects.filter(user=request.user,day=full_day).order_by('start_time')
              
              
               
                if constraint_obj:
                  
                
                    res=check_already_constraint(request,cours,constraint_obj)
                   
                   

                    if res == True:
                       
                        Allstudent.objects.create(user=request.user, course=cours, title=check)
                        if dday == 1:
                            already_cons=Constraint.objects.filter(user=request.user,name=constraint_, day=days, start_time = start_time_, end_time=end_time_)
                        elif dday ==2:
                            already_cons=Constraint.objects.filter(user=request.user,name=constraint_2, day=days_22, start_time = start_time_2, end_time=end_time_2)
                            
                        elif dday == 0:
                            already_cons=Constraint.objects.filter(user=request.user,name='m')
                        if already_cons:
                            continue
                        else:
                            if dday == 1:
                                check_constraint_to_add(request,constraint_,days, start_time_,end_time_)

                
                            elif dday ==2:
                                check_constraint_to_add(request,constraint_2,days_22,start_time_2, end_time_2)
        
                        return True
                    else:
                        continue
                        message1="constraint"
                else:
                   
                    Allstudent.objects.create(user=request.user, course=cours, title=check)

                    if dday == 1:
                        already_cons=Constraint.objects.filter(user=request.user,name=constraint_, day=days, start_time = start_time_, end_time=end_time_)
                    elif dday == 2:
                        already_cons=Constraint.objects.filter(user=request.user,name=constraint_2, day=days_22, start_time = start_time_2, end_time=end_time_2)
                    elif dday == 0:
                        already_cons=Constraint.objects.filter(user=request.user,name='m')

                    if already_cons:
                        pass
                    else:
                        if dday == 1:
                            check_constraint_to_add(request,constraint_,days, start_time_,end_time_)
                        elif dday ==2:
                            check_constraint_to_add(request,constraint_2,days_22,start_time_2, end_time_2)
        
                    
                  
                    return True
        else:
           
            if len(timetable) >=2:
                course_list = list(timetable)
                time_differences = []
                for course1, course2 in zip(course_list, course_list[1:]):
                    
                    if course1.end_time <= cours.start_time < course2.start_time and  course1.end_time <= cours.end_time <= course2.start_time:
                      
                        already_obj = Allstudent.objects.filter(user=request.user,title=check)
                        if already_obj:
                            continue
                        else:
                            constraint_obj=Constraint.objects.filter(user=request.user,day=full_day).order_by('start_time')
                            if constraint_obj:
                
                                res=check_already_constraint(request,cours,constraint_obj)
                                if res == True:
                                    Allstudent.objects.create(user=request.user, course=cours, title=check)
                                    if dday == 1:
                                        already_cons=Constraint.objects.filter(user=request.user,name=constraint_, day=days, start_time = start_time_, end_time=end_time_)
                                    elif dday ==2:
                                        already_cons=Constraint.objects.filter(user=request.user,name=constraint_2, day=days_22, start_time = start_time_2, end_time=end_time_2)
                                    elif dday == 0:
                                        already_cons=Constraint.objects.filter(user=request.user,name='m')
                                    if already_cons:
                                        pass
                                    else:
                                        if dday == 1:
                                            check_constraint_to_add(request,constraint_,days, start_time_,end_time_)
                                        elif dday ==2:
                                            check_constraint_to_add(request,constraint_2,days_22,start_time_2, end_time_2)
                        
                                    return True
                                else:
                                    message1="constraint"

                        
                    elif course1.end_time <=  cours.start_time >= course2.end_time or course2.end_time <=  cours.start_time  >= course1.end_time:
                       
                        constraint_obj=Constraint.objects.filter(user=request.user,day=full_day).order_by('start_time')
                        if constraint_obj:
                            res=check_already_constraint(request,cours,constraint_obj)
                            if res == True:
                                Allstudent.objects.create(user=request.user, course=cours, title=check)
                                if dday == 1:
                                    already_cons=Constraint.objects.filter(user=request.user,name=constraint_, day=days, start_time = start_time_, end_time=end_time_)
                                elif dday ==2:
                                    already_cons=Constraint.objects.filter(user=request.user,name=constraint_2, day=days_22, start_time = start_time_2, end_time=end_time_2)
                                elif dday == 0:
                                    already_cons=Constraint.objects.filter(user=request.user,name='m')
                                if already_cons:
                                    pass
                                else:
                                    if dday == 1:
                                        check_constraint_to_add(request,constraint_,days, start_time_,end_time_)
                                    elif dday ==2:
                                        check_constraint_to_add(request,constraint_2,days_22,start_time_2, end_time_2)
                                
                                return True
                            else:
                                message1="constraint"
                
            else:    
                timeta_ = timetable[0]
             
              
                if cours.start_time <= timeta_.start_time <= cours.end_time or  cours.start_time <= timeta_.end_time <= cours.end_time:

                    continue
                else:
                    if already_obj:
                        continue
                    else:
                        constraint_obj=Constraint.objects.filter(user=request.user,day=full_day).order_by('start_time')
                       
                        if constraint_obj:

            
                            res=check_already_constraint(request,cours,constraint_obj)
                            if res == True:
                                Allstudent.objects.create(user=request.user, course=cours, title=check)
                                if dday == 1:
                                    already_cons=Constraint.objects.filter(user=request.user,name=constraint_, day=days, start_time = start_time_, end_time=end_time_)
                                elif dday ==2:
                                    already_cons=Constraint.objects.filter(user=request.user,name=constraint_2, day=days_22, start_time = start_time_2, end_time=end_time_2)
                                elif dday == 0:
                                    already_cons=Constraint.objects.filter(user=request.user,name='m')
                                if already_cons:
                                    pass
                                else:
                                    if dday == 1:
                                        check_constraint_to_add(request,constraint_,days, start_time_,end_time_)
                                    elif dday ==2:
                                        check_constraint_to_add(request,constraint_2,days_22,start_time_2, end_time_2)
                    
                                return True
                            else:
                                message1="constraint"
                       
                        else:
                            
                            Allstudent.objects.create(user=request.user, course=cours, title=check)
                            if dday == 1:
                                already_cons=Constraint.objects.filter(user=request.user,name=constraint_, day=days, start_time = start_time_, end_time=end_time_)
                            elif dday ==2:
                                already_cons=Constraint.objects.filter(user=request.user,name=constraint_2, day=days_22, start_time = start_time_2, end_time=end_time_2)
                            elif dday == 0:
                                already_cons=Constraint.objects.filter(user=request.user,name='m')
                            if already_cons:
                                pass
                            else:
                                if dday == 1:
                                    check_constraint_to_add(request,constraint_,days, start_time_,end_time_)
                                elif dday ==2:
                                    check_constraint_to_add(request,constraint_2,days_22,start_time_2, end_time_2)
                            
                          
                            return True


    return False


@login_required
def get_index_page(request):
    course_ = Allcourse.objects.values('name').distinct()
 
    if request.user.is_superuser:
        #username = request.GET.get('username').strip()
       
        return render(request, 'user/index.html',context={'cource': course_})
    

    return render(request, 'user/index.html',context={'cource': course_})






'''
    This view take get and post Request 
    get for render cousres for user
    post for selecting courses and constraint 
 '''
@login_required
@api_view(['POST','GET'])
def select_courses(request): 
    '''
     below code for get  request and render the index page
    '''

    if request.method =='GET':
       
        course_ = Allcourse.objects.values('name').distinct()
        return render(request, 'user/index.html',context={'cource': course_})
    

   


    '''
     below code taking post request which have constraint and 
     course object which user is selecting

    '''
    data=request.data
    day = request.POST.get('day')
    checked_checkboxes_courses = request.POST.getlist('courses')
    start_time_ = request.POST['start_time']
    end_time_ = request.POST['end_time']
    constraint_ = request.POST['constraint']
    days=day.upper()
    days_=days[:3]
    day_2 = request.POST.get('day_2')
    days_2= day_2.upper()
    start_time_2 = request.POST['start_time_2']
    end_time_2 = request.POST['end_time_2']
    constraint_2 = request.POST['constraint_2']
    course_all= Allcourse.objects.values('name').distinct()
       
        
    message=''
    const_message =''
    
    if checked_checkboxes_courses == [] and day == '' and day_2 =='':
        course_ = Allcourse.objects.values('name').distinct()
        messageee ="You did not select any course and constraint"
        return render(request, 'user/index.html',context={'cource': course_ ,"errors":messageee})
   

    
    '''
     below code  for loop executing for courses which user selecting one and more 
     cousrses .for loop take course one by one course.
    '''
  
    if not checked_checkboxes_courses:
      
        if day:
            check_constraint_to_add(request,constraint_,days,start_time_,end_time_)
           
            exist_const= Constraint.objects.filter(user=request.user,name=constraint_, day=days, start_time = start_time_, end_time=end_time_)
            if exist_const.exists():
                pass
            else:
                const_message =const_message + constraint_
        if day_2:
            check_constraint_to_add(request,constraint_2,days_2,start_time_2,end_time_2)
            exist_const = Constraint.objects.filter(user=request.user,name=constraint_2, day=days_2, start_time = start_time_2, end_time=end_time_2)
            if exist_const.exists():
                pass
            else:
                const_message =const_message + constraint_


    else:  
        for check in checked_checkboxes_courses:  
            already_ = Allstudent.objects.filter(user=request.user,title=check)
            if already_:
                continue
            else:
                '''
                below code  for if user not selecting any constraint
                '''
                if not day:
                
                    course_= Allcourse.objects.filter(name=check)
                    if course_:
                        res=check_for_day(request,course_,check,0)
                        if res == False:
                            message1 = f"{check}"
                            message = message + message1 
                    else:
                        message1=f"{check}"
                        message=message+ message1                      
                            
                elif day:
                    
                    '''
                    below code execute when user select any constraint with courses
                    '''
                    course_= Allcourse.objects.filter(name=check ,day=days_)
                    if not course_:
                        course_= Allcourse.objects.filter(name=check).exclude(day=days_)
                
                    if course_.exists():
                    
                        course_ = course_.last()                
                        start_timee = time.fromisoformat(start_time_)
                        end_timeee = time.fromisoformat(end_time_)
                    
                    
                        if course_.start_time <= start_timee <= course_.end_time or course_.start_time <= end_timeee <= course_.end_time:
                            if day_2:
                                '''
                                    below code execute when user select any two constraint with courses
                                '''
                            
                                days_22=day_2.upper()
                                days_2=days_22[:3]
                                course_= Allcourse.objects.filter(name=check ,day=days_2).exclude(day=days_)
                                start_timee_2 = time.fromisoformat(start_time_2)
                                end_timee_2 = time.fromisoformat(end_time_2)       
                                if course_:
                                    for cours in course_:
                                        if cours.start_time <= start_timee_2 <= cours.end_time or cours.start_time <= end_timee_2 <= cours.end_time:
                                            course_= Allcourse.objects.filter(name=check).exclude(day=days_).exclude(day=days_2)
                                            if course_:
                                                check_for_day(request,course_,check,2)
                                            else: 
                                                message ="constrint"
                                                        
                                            
                                else:
                                    course_= Allcourse.objects.filter(name=check).exclude(day=days_).exclude(day=days_2)
        
                                    if course_:
                                        res =check_for_day(request,course_,check ,2)
                                        if res == False:
                                            message1 = f"{check}"
                                            message = message + message1   
                                    else:
                                        message1=f"{check}"
                                        message=message+ message1

                            else:
                                try:
                                        #first day and check another 
                                    course_= Allcourse.objects.filter(name=check).exclude(day=days_)
                                    if course_:
                                        res =check_for_day(request,course_,check,1)
                                        if res == False:
                                            message1 = f"{check}"
                                            message = message + message1   
                                    else:
                                        message1=f"{check}"
                                        message=message+ message1
                                    
                                except Exception as e :
                                    pass

                        else:
                            try:
                                course_= Allcourse.objects.filter(name=check).exclude(day=days_)
                                if course_:
                                    check_for_day(request,course_,check,1)              
                            except Exception as e:
                                pass
                        
                    else:
                        
                        message1=f"{check}"
                        
                        message = message +message1
                    
                
    '''
        below code execute w
    '''
    if checked_checkboxes_courses:
        if day:
                exist_const =  already_cons=Constraint.objects.filter(user=request.user,name=constraint_, day=day, start_time = start_time_, end_time=end_time_)
                if not exist_const:
                    const_message =const_message + constraint_
        if day_2:
                exist_const =  already_cons=Constraint.objects.filter(user=request.user,name=constraint_2, day=day_2, start_time = start_time_2, end_time=end_time_2)
                if not exist_const:
                    const_message =const_message + constraint_
    new =''
    constraint_message = ''
  
    if const_message!='' or message != '':
        course_ = Allcourse.objects.values('name').distinct()
        if message:
            message ="you can not take course "+message +" due to constraint"
        if const_message:
            constraint_message="you can not add that constaint"+const_message +" due to course or constraint"
        return render(request, 'user/index.html',context={'cource': course_, "errors":new ,'const_errors':constraint_message})
    else:
        print("hussain")
       
        return  redirect('user:show_timetable')
    
   

   
    
'''
    It shows the time table for student
 '''   
@login_required
@api_view(['GET'])
def show_timetable(request):

    allstudent=Allstudent.objects.filter(user=request.user)    
    timetable = Allcourse.objects.filter(allstudent__user=request.user).order_by('start_time')
    serializer_data = UserSerializerForTimeTable(timetable,many=True ,context={'request': request})

    # Sort the data by 'day' field
    sorted_data = sorted(serializer_data.data, key=itemgetter('day'))

    # Group the data by 'day' field
    grouped_data = groupby(sorted_data, key=itemgetter('day'))

    # Create a dictionary with 'day' as keys and grouped data as values
    grouped_dict = {key: list(group) for key, group in grouped_data}
    #sorted_dict = {key: grouped_dict[key] for key in sorted(grouped_dict.keys())}

    days = {"SUN":1, "MON":2, "TUE":3, "WED":4, "THU":5, "FRI":6}
    days_2 = {1:"SUNDAY", 2:"MONDAY", 3:'TUESDAY', 4:"WEDNESDAY", 5:'THURSDAY', 6:'FRIDAY'}
    g_d = {i : [] for i in range(1,7)}
    for key in days:
        if key in  grouped_dict:
            g_d[days[key]] = grouped_dict[key]
        
 
    

   
    for k,v in g_d.items():
        if not v:
            empyt_day = days_2[k]
            const_obj = Constraint.objects.filter(user=request.user,day=empyt_day)
            dict_list = list(const_obj.values())
            if dict_list:
                g_d[k] = [{"const_obj":dict_list}]
    #print("GD    ",g_d)
    #pdb.set_trace()
        # else:
        #     full_day=days_2[key]
        #     obj=Constraint.objects.filter(user=request.user,day=full_day)
        #     if obj:
        #         obj.delete()

    sorted_dict = {}
    for k in g_d:
        obj_list = []
        first = True
        for i in g_d[k]:
            obj = {}
            for j in i:
                if j =='const_obj':
                    if first:
                        for l in i[j]:
                            obj_list.append({'const_obj' : l})
                else:
                    obj[j] = i[j]
            if obj:
                obj_list.append({'object' : obj})
            first = False
        sorted_dict[k] = sorted(obj_list, key = lambda x:[str(x[y]['start_time']).replace(':','') for y in x])
    
    for key, values in sorted_dict.items():
        for item in values:
            if 'object' in item:
                start_time_str = item['object']['start_time']
                end_time_str = item['object']['end_time']
            else:
                continue
            start_time_object = datetime.strptime(start_time_str, '%H:%M:%S')
            end_time_object = datetime.strptime(end_time_str, '%H:%M:%S')
            hour = start_time_object.hour
            minute = start_time_object.minute

            # Create a datetime.time object
            start_time = time(hour, minute)


            # Extract the hour and minute components
            hour = end_time_object.hour
            minute = end_time_object.minute

            # Create a datetime.time object
            end_time = time(hour, minute)
            item['object']['start_time'] = start_time
            item['object']['end_time'] = end_time
  
    return render(request, 'user/timetable.html',{'grouped_dict': g_d ,'data':sorted_dict})
 
