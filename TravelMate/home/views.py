from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')    
def userLogin(request):
    return render(request,'user/userLogin.html') 
def userReg(request):  
    if request.method=="POST":
        Name = request.POST.get("Name") 
        email = request.POST.get("email")
        phonenumber = request.POST.get("phonenumber")   # FIXED
        password = request.POST.get("password") 
        confirmpassword = request.POST.get("confirmpassword") 

        if password == confirmpassword:
            if userRegistration.objects.filter(email=email).exists():
                messages.info(request,'This email is already in use')
            elif userRegistration.objects.filter(phoneNumber=phonenumber).exists():
                messages.info(request,'This Phone Number is already in use')
            else:
                userdata = userRegistration(
                    Name=Name,
                    email=email,
                    phoneNumber=phonenumber,
                    password=password
                )
                userdata.save()
                return redirect(userLogin)
    return render(request,'user/userReg.html')


    return render(request,'user/userReg.html')

    return render(request,'user/userReg.html')
def userHome(request):      
    return render(request,'user/userHome.html')  
def about(request):
    return render(request,'user/about.html')
def coTraveler(request):
    return render(request,'user/coTraveller.html')
def userProfile(request):
    return render(request,'user/userProfile.html')
def hireDriver(request):
    return render(request,'user/hireDriver.html')
def hireNow(request):
    return render(request,'user/hireNow.html')
def rentCar(request):
    return render(request,'user/rentCar.html')
def rentNow(request):
    return render(request,'user/rentNow.html')
def destination(request):
    return render(request,'user/desination.html')