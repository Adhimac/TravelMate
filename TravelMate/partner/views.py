from django.shortcuts import render

# Create your views here.
def driverLogin(request):   
    return render(request,'partner/driverLogin.html')   
def driverRegister(request):    
    return render(request,'partner/driverRegister.html')
def driverHome(request):    
    return render(request,'partner/driverHome.html')    

 