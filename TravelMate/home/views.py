from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')    
def userLogin(request):
    return render(request,'user/userLogin.html') 
def userReg(request):   
    return render(request,'user/userReg.html')
def userHome(request):      
    return render(request,'user/userHome.html')  
def about(request):
    return render(request,'user/about.html')
def destination(request):
    return render(request,'user/destination.html')
def coTraveler(request):
    return render(request,'user/coTraveller.html')
