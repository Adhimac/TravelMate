from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.
def driverLogin(request):   
     if request.method=="POST":
        try:
            email=request.POST.get("email")
            password=request.POST.get("password")
            log=driverRegistration.objects.get(email=email,password=password)
            request.session['firstname']=log.name
            request.session['id']=log.id
            return redirect("driverHome")
        except driverRegistration.DoesNotExist as e :
            messages.info(request,'invalid login')
     return render(request,'partner/driverLogin.html')   
def driverRegister(request):   
    if request.method == "POST":  
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")
        licenseNumber = request.POST.get("licenseNumber")
        aadharId = request.POST.get("aadharId")

        if password != confirmPassword:
            messages.error(request, "Passwords do not match")
            return redirect("driverRegister")
        if driverRegistration.objects.filter(email=email).exists():
            messages.error(request, "This email is already in use")
            return redirect("driverRegister")
        userdata = driverRegistration(
            name=name,
            email=email,
            password=(password),
            licenceNumber=licenseNumber,
            aadharId=aadharId,
        )
        userdata.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect("driverLogin")

    return render(request, 'partner/driverRegister.html')

def driverHome(request):    
    return render(request,'partner/driverHome.html')    
def driverProfile(request):
    return render(request,'partner/driverProfile.html')

 