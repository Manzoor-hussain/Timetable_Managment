from base64 import urlsafe_b64decode, urlsafe_b64encode
from email.message import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password



from django.utils.encoding import force_bytes
from django.core import serializers
from .models import Allcourse




# Create your views here.
@login_required
def get_index_page(request):
    course_ = Allcourse.objects.values('name').distinct()
    if request.user.is_superuser:
        
       
        return render(request, 'user/index.html',context={'cource': course_})
    

    return render(request, 'user/index.html',context={'cource': course_})
@api_view(['POST','GET'])
def login_page(request):
    if request.method == 'GET':
        user_ = request.user
        if user_.username:
            response = redirect('user:dashboard')
            return response
        else:
            error_message = ''
            return render(request, 'superadmin/auth/login.html', {'error_message': error_message})
        
   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_ = authenticate(username=username, password=password)
        if user_:
            login(request, user_)
           
            if user_.is_superuser:
                response = redirect('user:dashboard')
            else:
                response = redirect('user:dashboard')
            response.set_cookie(key='name', value=user_.email)
            response.set_cookie(key='email', value=user_.username)
            
            return response
        else:
            error_message = 'Invalid username or password'
            return render(request, 'superadmin/auth/login.html', {'error_message': error_message})

@api_view(['POST','GET'])
def register_page(request):
    if request.method == 'GET':
        user_ = request.user
        if user_.username:
            response = redirect('user:dashboard')
            return response
        else:
            return render(request, 'superadmin/auth/register.html')
        
    

    if request.method == 'POST':
        name_ = request.POST['full_name']
        email = request.POST['email'].lower().strip()
        password = request.POST['password']
      

        if User.objects.filter(username=email).exists():
            return JsonResponse(status=400, data={'error': 'This email address already registered'})

        uu = User.objects.create(first_name=name_, email=email, username=email)
        uu.set_password(password)
        uu.save()
       
      
       
       

    response = render(request, 'superadmin/auth/register.html')
    return response


@login_required
def logout_page(request):
   
    response = redirect('/login')  # Redirect to the desired page after logout
    # Set cookies to expire in the past
    response.delete_cookie('name')
    response.delete_cookie('email')
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    logout(request)
    
    
    return response
    




