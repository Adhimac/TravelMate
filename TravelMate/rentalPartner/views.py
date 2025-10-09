from django.shortcuts import render

# Create your views here.
def rentalPartnerLogin(request):   
    return render(request,'rentalPartner/rentalPartnerLogin.html')  
def rentalPartnerRegister(request):   
    return render(request,'rentalPartner/rentalPartnerRegister.html')
def rentalPartnerHome(request):   
    return render(request,'rentalPartner/rentalPartnerHome.html')