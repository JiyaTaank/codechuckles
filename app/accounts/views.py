from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_POST



def register_user(request):

    if request.method=='POST':

        username = request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'User with this username already exists')
            return redirect("/auth/register/")
        
        user=User.objects.create_user(username=username)
        user.set_password(password)
        user.save()

        messages.success(request,'User created successfully')
        return redirect('/auth/login/')
    
    
    return render(request,'register.html')

def login_user(request):
     if request.method=='POST':

        username = request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,'User with this username does not exist')
            return redirect('/auth/login/')
        
        user= authenticate(username=username,password=password)

        if user is None:
            messages.info(request,'Invalid Username OR Password')
            return redirect('/auth/login')
        
        login(request,user)
        
        return redirect('/home/questions/')
     
    
     return render(request, 'login.html')

@require_POST
def logout_user(request):
    logout(request)
    messages.success(request,'Logout successful')
    return redirect('/auth/login/')
        



        