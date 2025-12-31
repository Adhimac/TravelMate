from django.shortcuts import render,redirect, get_object_or_404

from rentalPartner.models import *
from . models import *
from django.contrib import messages
from partner.models import *

# Create your views here.
def index(request):
    return render(request,'index.html')    
def userLogin(request):
    if request.method=="POST":
        try:
            email=request.POST.get("email")
            password=request.POST.get("password")
            log=userRegistration.objects.get(email=email,password=password)
            request.session['firstname']=log.Name
            request.session['id']=log.id
            return redirect("userHome")
        except userRegistration.DoesNotExist as e :
            messages.info(request,'invalid login')
    return render(request,'user/userLogin.html') 
def userReg(request):  
    if request.method=="POST":
        Name = request.POST.get("Name") 
        email = request.POST.get("email")
        phonenumber = request.POST.get("phoneNumber")   # FIXED
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
                return redirect("userLogin")
    return render(request,'user/userReg.html')
def userHome(request):     
     
    return render(request,'user/userHome.html')  
def about(request):
    return render(request,'user/about.html')
def coTraveler(request):
    travelers = userRegistration.objects.order_by('registrationDate')[:3]
    return render(request,'user/coTraveller.html' , {'travelers': travelers})
def userProfile(request):
    return render(request,'user/userProfile.html')
def hireDriver(request):
    drivers = driverRegistration.objects.all()
    return render(request,'user/hireDriver.html', {'drivers': drivers})
def hireNow(request,driver_id):
    driver = driverRegistration.objects.get(id=driver_id)
    return render(request,'user/hireNow.html', {'driver': driver})
def rentCar(request):
    cars = carDetails.objects.all()
    return render(request,'user/rentCar.html', {'cars': cars})
def rentNow(request,car_id):
    car = carDetails.objects.get(id=car_id)
    us=userRegistration.objects.get(id=request.session['id'])
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        phone_number = request.POST.get("phone")
        pickupLocation = request.POST.get("pickupLocation")
        dropLocation = request.POST.get("dropLocation")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        numberOfDays = request.POST.get("numberOfDays")
        preferredTime = request.POST.get("preferredTime")
        notes = request.POST.get("notes")

        booking = bookingDetails(
            
            user_id=request.session['id'],
            partner_id=car.partner.id,
            car_id=car.id,
            Name=customer_name,
            phoneNumber=phone_number,
            pickupLocation=pickupLocation,
            dropLocation=dropLocation,
            startDate=startDate,
            endDate=endDate,
            numberOfDays=numberOfDays,
            preferredTime=preferredTime,
            carRentPerDay=car.rentPerDay,
            carName=car.vehicleName,
            Additionalnotes=notes,
            bookingStatus=True
        )
        booking.save()
        messages.success(request, 'Booking successful!')
        # return redirect('user/payment.html')
    return render(request,'user/rentNow.html', {'car': car, 'us': us})
def destination(request):
    return render(request,'user/desination.html')
def payment(request):
    return render(request,'user/payment.html')
# def profileList(request):
#     travelers = userRegistration.objects.all()
#     return render(request, 'user/profileList.html' , {'travelers': travelers})
def profileDetail(request, user_id):
    traveler = userRegistration.objects.get(id=user_id)
    return render(request, 'user/profileDetails.html', {'traveler': traveler})


from django.shortcuts import render
from django.db.models import Q
from .models import userRegistration

def profileList(request):
    travelers = userRegistration.objects.all()

    q = request.GET.get('q')
    destination = request.GET.get('destination')
    gender = request.GET.get('gender')

    # 🔍 FILTER BY USER NAME (MAIN REQUIREMENT)
    if q:
        travelers = travelers.filter(Name__icontains=q)

    # OPTIONAL FILTERS
    if destination:
        travelers = travelers.filter(destination=destination)

    if gender:
        travelers = travelers.filter(gender=gender)

    return render(request, 'user/profileList.html', {
        'travelers': travelers
    })
def connect_traveler(request, user_id):
    traveler = get_object_or_404(userRegistration, id=user_id)

    traveler.connected = True
    traveler.save()

    return redirect('profileDetail', user_id=traveler.id)