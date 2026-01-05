from django.shortcuts import render

from partner.models import *
from .models import *
from home.models import *
from rentalPartner.models import *


# Create your views here.
def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            admin = proAdmin.objects.get(username=username, password=password)
            return render(request, 'appadmin/adminHome.html')
        except proAdmin.DoesNotExist:
            error_message = "Invalid username or password."
            return render(request, 'appadmin/adminLogin.html', {'error_message': error_message})  
    return render(request, 'appadmin/adminLogin.html')  

def adminHome(request):
    return render(request, 'appadmin/adminHome.html')
def adminUserManagement(request):
    users = userRegistration.objects.all()
    return render(request, 'appadmin/adminUserManagement.html', {'users': users})
def adminDriverManagement(request):
    drivers = driverRegistration.objects.all()

    return render(request, 'appadmin/adminDriverManagement.html', {'drivers': drivers})
def adminCarManagement(request):
    cars = carDetails.objects.all()
    return render(request, 'appadmin/adminCarManagement.html', {'cars': cars})
def viewBookings(request):
    bookings = bookingDetails.objects.all()
    return render(request, 'appadmin/viewBooking.html', {'bookings': bookings})