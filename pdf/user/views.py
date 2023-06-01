from django.http import Http404, HttpResponse
from django.shortcuts import render ,redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import PdfSerializer, StorefileSerializer, UserSerializerForTimeTable
from rest_framework.response import Response
from rest_framework import status
from .models import Pdf, Storefile
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.db.models import Case, When, IntegerField
from django.db.models.functions import ExtractWeekDay
from django.db.models import Func
import datetime



from django.http import FileResponse
from django.contrib.auth.models import User
from django.conf import settings
from superadmin.models import Service, Myservice, Mypermission, Countservices, Course, Timetable, Student, Allcourse, Allstudent, Constraint
from .serializers import UserSerializerForCount
import os
from  datetime import time
from itertools import groupby
from operator import itemgetter
from collections import OrderedDict
import pdb

# Create your views here.
def myconstraint(request,cours,constraint_obj):
    print(":request myconstraint")
   
    if cours:
                 
        for const in constraint_obj:
            if const.end_time <= cours.start_time or const.start_time<=cours.end_time:
            #if cours.start_time >= const.start_time <=cours.end_time or cours.start_time <= const.end_time <=cours.end_time:
                print("in")
                return True
            else:
                continue
        return  False
    
   
def check_constraint_to_add(request,name,day,start_time,end_time):
    days = day[:3]
   
    constraint__=Constraint.objects.filter(day=days)
    start_timee_2 = time.fromisoformat(start_time)
    end_timee_2 = time.fromisoformat(end_time)

    if constraint__:
       
        for cont in constraint__:

            if cont.start_time <= start_timee_2 <= cont.end_time or cont.start_time <= end_timee_2 <= cont.end_time:
                continue
            else:
                student=Allstudent.objects.filter(day=days)
                if student:
                    for stu in student:
                        if stu.start_time <= start_timee_2 <=stu.end_time or  stu.start_time <= end_timee_2 <=stu.end_time:
                            continue
                        else:
                            already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                            if already_cons:
                                continue
                            else:
                                myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                            break
                else:
                    already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                    if already_cons:
                        continue
                    else:
                        myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                    break
    else:
        
        allstudent=Allstudent.objects.filter(user=request.user) 
        student = Allcourse.objects.filter(allstudent__user=request.user,day=days)
      
        if student:
            if len(student) == 1:

                for stu in student:
                    if stu.start_time <= start_timee_2 <=stu.end_time or  stu.start_time <= end_timee_2 <=stu.end_time:
                        continue
                    else:
                        already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                        if already_cons:
                            continue
                        else:
                            myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                        break
            
            elif len(student) >= 2:
               # res=check_for_day(request,course_,check,0)

            
                course_list = list(student)
                
                for cours in student:

                    time_differences = []
                    for course1, course2 in zip(course_list, course_list[1:]):
                        
                        if course1.end_time <= start_timee_2 < course2.start_time and  course1.end_time <= end_timee_2 <= course2.start_time:
                            print("created")
                            already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                            if already_cons:
                                continue
                            else:
                                myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                            break
                        elif course1.end_time <= start_timee_2 >= course2.end_time or course2.end_time <= start_timee_2 >= course1.end_time:
                            already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                            if already_cons:
                                continue
                            else:
                                myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                            break
                           
                            
                                
                
        else:

            already_cons=Constraint.objects.filter(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
            if already_cons:
                pass
            else:
                myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
           
            



                





def check_for_day(request,course_,check,dday):
    day = request.POST.get('day')
    day_2 = request.POST.get('day_2')
   # course= request.POST.get('courses')
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
    count=0
    for cours in course_:
        print("inside foor loop day not match")
        already_obj = Allstudent.objects.filter(user=request.user,title=check)
        allstudent=Allstudent.objects.filter(user=request.user) 
        timetable = Allcourse.objects.filter(allstudent__user=request.user,day=cours.day)
        days_2 = {"MON":"MONDAY", "TUE":'TUESDAY', "WED":"WEDNESDAY", "THU":'THURSDAY', "FRI":'FRIDAY',"SUN":'SUNDAY'}
        full_day=''
       
        count=count+1
        if cours.day in days_2:
            full_day = days_2[cours.day]

        print("how many tim",len(course_),cours.day,count)
        if not timetable:
            
            if already_obj:
                continue
            else:
                constraint_obj=Constraint.objects.filter(user=request.user,day=full_day)
              
                print("at first")
               
                if constraint_obj:
                    print("constriant",constraint_obj)
                
                    res=myconstraint(request,cours,constraint_obj)
                    print("constaint resuls",res)
                   

                    if res == True:
                        pdb.set_trace()
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
                  
                    print("khan")
                    pdb.set_trace()
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
        
                    
                    print("not time table")
                    return True
        else:
           
            if len(timetable) >=2:
                course_list = list(timetable)
                time_differences = []
                for course1, course2 in zip(course_list, course_list[1:]):
                    
                    if course1.end_time <= cours.start_time < course2.start_time and  course1.end_time <= cours.end_time <= course2.start_time:
                        print("created object betwnn")
                        already_obj = Allstudent.objects.filter(user=request.user,title=check)
                        if already_obj:
                            continue
                        else:
                            constraint_obj=Constraint.objects.filter(user=request.user,day=full_day)
                            if constraint_obj:
                
                                res=myconstraint(request,cours,constraint_obj)
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

                        #myob = Constraint.objects.create(user=request.user,name=name, day=day, start_time = start_time, end_time=end_time)
                    elif course1.end_time <=  cours.start_time >= course2.end_time or course2.end_time <=  cours.start_time  >= course1.end_time:
                        print("created object at the end")
                        constraint_obj=Constraint.objects.filter(user=request.user,day=full_day)
                        if constraint_obj:
                            res=myconstraint(request,cours,constraint_obj)
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
                if count == 3:
                    pdb.set_trace()
              
                if cours.start_time <= timeta_.start_time <= cours.end_time or  cours.start_time <= timeta_.end_time <= cours.end_time:
                    print("match continur")
                    continue
                else:
                    if already_obj:
                        continue
                    else:
                        constraint_obj=Constraint.objects.filter(user=request.user,day=full_day)
                       
                        if constraint_obj:

            
                            res=myconstraint(request,cours,constraint_obj)
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
                            
                            print("not time  under 495 table")
                            return True


    return False


@login_required
def get_index_page(request):
    course_ = Allcourse.objects.values('name').distinct()
   
 
    if request.user.is_superuser:
        #username = request.GET.get('username').strip()
        services_ = Myservice.objects.all()
        return render(request, 'superadmin/index.html',context={'service': services_})
    

    return render(request, 'user/index.html',context={'cource': course_})

# @api_view(['GET'])
# def index(request):
#     file=Pdf.objects.get(id=5)
#     return render(request, 'user/index.html', context={"file":file})

@api_view(['GET'])
@login_required
def upload_file(request ,service):
    return render(request, 'user/upload_file.html', context={"service_name":service})
    

@login_required
@api_view(['POST','GET'])
def perform_services(request): 

    if request.method =='GET':
        #return redirect('user:dashboard')
        print("hussain")
        course_ = Allcourse.objects.values('name').distinct()
        return render(request, 'user/index.html',context={'cource': course_})
    

   
    data=request.data
    day = request.POST.get('day')
    day_2 = request.POST.get('day_2')
   # course= request.POST.get('courses')
    checked_checkboxes = request.POST.getlist('courses')

   

    start_time_ = request.POST['start_time']
    end_time_ = request.POST['end_time']
    constraint_ = request.POST['constraint']
    
    days=day.upper()
    days_=days[:3]
   
    start_time_2 = request.POST['start_time_2']
    end_time_2 = request.POST['end_time_2']
    constraint_2 = request.POST['constraint_2']
    course_all= Allcourse.objects.values('name').distinct()
       
        
    message=''

    for check in checked_checkboxes:  
        already_ = Allstudent.objects.filter(user=request.user,title=check)
        if already_:
            continue
        else:
            if not day:
                print("empty")
                course_= Allcourse.objects.filter(name=check)
                if course_:
                    res=check_for_day(request,course_,check,0)
                    if res == False:
                        message1 = f"{check}"
                    
                        message = message + message1 
                else:
                    message1=f"{check}"
                    message=message+ message1                      
                    
                    """THis is code for when User have no constrint"""    
            elif day:
                print("day hai")
                course_= Allcourse.objects.filter(name=check ,day=days_)
                if not course_:
                    course_= Allcourse.objects.filter(name=check).exclude(day=days_)
            
                if course_.exists():
                    print("exist")
                    course_ = course_.last()                
                    start_timee = time.fromisoformat(start_time_)
                    end_timeee = time.fromisoformat(end_time_)
                    print("here")
                  
                    if course_.start_time <= start_timee <= course_.end_time or course_.start_time <= end_timeee <= course_.end_time:
                        if day_2:
                            print("days2")
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
                                            print("check call for day2")
                                            check_for_day(request,course_,check,2)
                                        else: 
                                            message ="constrint"
                                            print("no objects")               
                                        
                            else:
                                course_= Allcourse.objects.filter(name=check).exclude(day=days_).exclude(day=days_2)
    
                                if course_:
                                    print("check For day2")
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
                                    print("check for day1")
                                    res =check_for_day(request,course_,check,1)
                                    if res == False:
                                        message1 = f"{check}"
                                    
                                        message = message + message1   
                                else:
                                    message1=f"{check}"
                                    message=message+ message1
                                 
                            except Exception as e :
                                print("exception",e)
                           
                                pass

                    else:
                        try:

                            print("time condition false bach gea constr day1")
                            course_= Allcourse.objects.filter(name=check).exclude(day=days_)
                            if course_:
                                print("check for day 1")
                                check_for_day(request,course_,check,1)              
                        except Exception as e:
                            print("exceptio All student",e)
                            pass
                       
                else:
                    
                    message1=f"{check}"
                    
                    message = message +message1
                    print("final")
                
                
   

    
    if message:
        course_ = Allcourse.objects.values('name').distinct()
        new ="you can not take course "+message +" due to constraint"
        print("course last",course_)
       
        return render(request, 'user/index.html',context={'cource': course_, "errors":new})
        

    else:
        return  redirect('user:show_timetable')
    
   

   
    
    #return render(request, 'user/upload_file.html',context={'studentrecord':"dds" ,"timetables":timetable,"timetable_data":timetable_data,"stu":stu})
@login_required
@api_view(['GET'])
def show_timetable(request):

   
    allstudent=Allstudent.objects.filter(user=request.user)
   
  
    
    timetable = Allcourse.objects.filter(allstudent__user=request.user).order_by('start_time')
    

    ss = UserSerializerForTimeTable(timetable,many=True ,context={'request': request})



    # Sort the data by 'day' field
    sorted_data = sorted(ss.data, key=itemgetter('day'))

    # Group the data by 'day' field
    grouped_data = groupby(sorted_data, key=itemgetter('day'))

    # Create a dictionary with 'day' as keys and grouped data as values
    grouped_dict = {key: list(group) for key, group in grouped_data}
    #sorted_dict = {key: grouped_dict[key] for key in sorted(grouped_dict.keys())}

    # print("sorted",sorted_dict)

   # print("group last Final",grouped_dict)

    # Print the grouped dictionary
    context = {}

    # for day, group in grouped_dict.items():
    #     #print("days",day,group)
    #     context[day] = list(group)

    #print("context:", context)

    # context ={}
    # for day, group in grouped_dict.items():
    #     print("day",day)
    #     for item in group:
           
    #         print("item",item)
   
    days = {"MON":1, "TUE":2, "WED":3, "THU":4, "FRI":5, "SUN":7}
    days_2 = {"MON":"MONDAY", "TUE":'TUESDAY', "WED":"WEDNESDAY", "THU":'THURSDAY', "FRI":'FRIDAY',"SUN":'SUNDAY'}
    for key in days:
        if key in  grouped_dict:
            grouped_dict[days[key]] = grouped_dict[key]
            del grouped_dict[key]
    print("gropu",grouped_dict)
    # pdb.set_trace()
        # else:
        #     full_day=days_2[key]
        #     obj=Constraint.objects.filter(user=request.user,day=full_day)
        #     if obj:
        #         obj.delete()

  
    # for day, group in grouped_dict.items():
    #     print("day",day,group)

      
        # for item in group:
        #     print("day"+item)
           
           
           

   
    # print("context",context)
   
   
    return render(request, 'user/upload_file.html',{'grouped_dict': grouped_dict})
 


   

api_view(['GET'])
@login_required
def download_docx(request):
    title = request.GET.get('title').strip()
    pass
   
  