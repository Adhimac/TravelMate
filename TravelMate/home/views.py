import random
from django.shortcuts import render,redirect, get_object_or_404
from urllib3 import request
from rentalPartner.models import *
from . models import *
from django.contrib import messages
from partner.models import *
from django.core.mail import send_mail
from django.conf import settings
global amount

from TravelMate.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay

# Create your views here.
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from rentalPartner.models import carDetails
from .models import userRegistration, driverBooking

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))

def Booking(request):
    # Logged in user
    user_id = request.session.get('id')
    if not user_id:
        return redirect("userLogin")

    # Fetch user
    user = userRegistration.objects.get(id=user_id)

    # Fetch URL params
    a = request.GET.get('amount')
    destination = request.GET.get('destination')
    date = request.GET.get('date')
    users = request.GET.get('passengers')

    if not a:
        return redirect("rentCar")

    # Convert INR → paise
    razor_amount = int(a) * 100  

    # Create Razorpay order
    order = client.order.create({
        "amount": razor_amount,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "a": a,
        "razor_amount": razor_amount,
        "order_id": order["id"],
        "api_key": settings.RAZORPAY_API_KEY,

        # Trip details
        "destination": destination,
        "date": date,
        "users": users,

        # User details (from session model)
        "userName": user.Name,
        "userEmail": user.email,
        "userPhone": user.phoneNumber,
    }

    return render(request, "user/booking.html", context)

   



def cart(request):
    ud=request.session['id']
    menu=driverBooking.objects.filter(user=ud,checkout_status=False)
    sum=0       
    for i in menu:
            sum += int(i.price) * int(i.quan)
            global amount
            amount=sum
    return render(request,'user/cart.html',{'menu':menu,'sum':sum})

def cartdel(request,kid):
    carte = driverBooking.objects.get(id=kid)
    carte.delete()
    return redirect("cart")



client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
def bookingpay(request):
    global amount
    api_key=RAZORPAY_API_KEY
    amt=int(amount)*100
    currency = "INR"
  
    payment_order = client.order.create(dict(amount=amt, currency="INR", payment_capture=1))
    payment_order_id = payment_order['id']
    driverBooking.objects.filter(user=request.session['id']).update(checkout_status=True)
    return render(request, 'user/bookingpay.html', {'a': amount, 'api_key': api_key, 'order_id': payment_order_id})
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
        profileImage = request.FILES.get("profileImage")

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
                    password=password,
                    profileImage=profileImage
                    
                )
                userdata.save()
                return redirect("userLogin")
    return render(request,'user/userReg.html')
def userHome(request):     
     
    return render(request,'user/userHome.html')  
def about(request):
    return render(request,'user/about.html')
# def coTraveler(request):
#     travelers = userRegistration.objects.order_by('registrationDate')[:3]
#     return render(request,'user/coTraveller.html' , {'travelers': travelers})


def userProfile(request):
    user = userRegistration.objects.get(id=request.session['id'])
    return render(request,'user/userProfile.html', {'user': user})
def hireDriver(request):
    drivers = driverRegistration.objects.all()

    return render(request,'user/hireDriver.html', {'drivers': drivers})
def hireNow(request, id):
    # get selected driver
    driver = get_object_or_404(driverRegistration, id=id)

    # get logged-in user
    user_id = request.session.get('id')
    user = get_object_or_404(userRegistration, id=user_id)

    # get driver's car (adjust if driver has multiple cars)
    car = carDetails.objects.filter(driver=driver).first()

    if request.method == "POST":

        # ----------- FORM DATA -----------
        pickupLocation = request.POST.get('pickupLocation')
        dropLocation = request.POST.get('dropLocation')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        preferredTime = request.POST.get('preferredTime')
        paymentMethod = bool(int(request.POST.get('paymentMethod')))

        # ----------- DATE CALCULATION -----------
        start = datetime.strptime(startDate, "%Y-%m-%d").date()
        end = datetime.strptime(endDate, "%Y-%m-%d").date()
        numberOfDays = (end - start).days + 1

        if numberOfDays <= 0:
            return render(request, 'hire_now.html', {
                'driver': driver,
                'error': 'End date must be after start date'
            })

        # ----------- SAVE BOOKING -----------
        booking = driverBooking(    
            driver=driver,
            user=user,
            car=car,
            pickupLocation=pickupLocation,
            dropLocation=dropLocation,
            startDate=start,
            endDate=end,
            numberOfDays=numberOfDays,
            preferredTime=preferredTime,
            bookingDate=timezone.now(),
            paymentMethod=paymentMethod,
            confirmStatus=False,
            bookingStatus=False,
            fareperday=car.pricePerDay if car else 0,
            carName=car.carName if car else "N/A"
        )
        booking.save()

        return redirect('driverBookings')

    # ----------- GET REQUEST -----------
    return render(request, 'hire_now.html', {
        'driver': driver,
        'car': car
    })
def rentCar(request):
    cars = carDetails.objects.all()
    return render(request,'user/rentCar.html', {'cars': cars})

# def rentNow(request, car_id):
#     car = carDetails.objects.get(id=car_id)
#     us = userRegistration.objects.get(id=request.session['id'])

#     if request.method == "POST":
#         customer_name = request.POST.get("customer_name")
#         phone_number = request.POST.get("phone")
#         pickupLocation = request.POST.get("pickupLocation")
#         dropLocation = request.POST.get("dropLocation")
#         startDate = request.POST.get("startDate")
#         endDate = request.POST.get("endDate")
#         numberOfDays = request.POST.get("numberOfDays")
#         preferredTime = request.POST.get("preferredTime")
#         notes = request.POST.get("notes")

#         # Calculate total amount
#         price_per_day = car.rentPerDay
#         total_amount = int(numberOfDays) * price_per_day

#         # Save booking here
#         booking = bookingDetails.objects.create(
#             user_id=request.session['id'],
#             partner_id=car.partner.id,
#             car_id=car.id,
#             Name=customer_name,
#             phoneNumber=phone_number,
#             pickupLocation=pickupLocation,
#             dropLocation=dropLocation,
#             startDate=startDate,
#             endDate=endDate,
#             numberOfDays=numberOfDays,
#             preferredTime=preferredTime,
#             carRentPerDay=price_per_day,
#             carName=car.vehicleName,
#             Additionalnotes=notes,
#             bookingStatus=True,
#         )

        # Now redirect to Razorpay payment page
        # return redirect(
        #     f"/booking?amount={total_amount}&destination={pickupLocation}&date={startDate}&passengers=1"
        # )

    # return render(request, 'user/rentNow.html', {'car': car, 'us': us})

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
    return render(request,'user/rentNow.html', {'car': car, 'us': us})
def destination(request):
    return render(request,'user/desination.html')
def payment(request):
    return render(request,'user/payment.html')
# def profileList(request):
#     travelers = userRegistration.objects.all()
#     return render(request, 'user/profileList.html' , {'travelers': travelers})
def profileDetail(request, user_id):
    current_user_id = request.session['id']

    # 1) Fetch complete user details
    other_user = get_object_or_404(userRegistration, id=user_id)

    # 2) Fetch connection flags separately
    is_connected = connectedTravelers.objects.filter(
        traveler_id=current_user_id,
        connected_traveler_id=user_id,
        connected=True,
        connected_accepted=True,
    ).exists()

    is_pending = connectedTravelers.objects.filter(
        traveler_id=current_user_id,
        connected_traveler_id=user_id,
        connected=True,
        connected_accepted=False,
    ).exists()

    # 3) Past trips placeholder
    user_trips = []

    return render(request, 'user/profileDetails.html', {
        'other_user': other_user,
        'is_connected': is_connected,
        'is_pending': is_pending,
        'user_trips': user_trips,
    })
def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = userRegistration.objects.get(email=email)

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Store OTP in session
            request.session['reset_email'] = email
            request.session['reset_otp'] = otp

            # Send email
            send_mail(
                subject='Your Password Reset OTP',
                message=f"Hello {user.Name},\nYour OTP is: {otp}\nUse this to reset your password.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email")
            return redirect('verifyOTP')

        except userRegistration.DoesNotExist:
            messages.error(request, "Email not found")
            return redirect('forgotPassword')

    return render(request, 'user/forgotPassword.html')


def verifyOTP(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        saved_otp = str(request.session.get('reset_otp'))

        if entered_otp == saved_otp:
            return redirect('resetPassword')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('verifyOTP')

    return render(request, 'home/verifyOTP.html')
def resetPassword(request):
    email = request.session.get('reset_email')

    if not email:
        return redirect('forgotPassword')

    if request.method == "POST":
        new_password = request.POST.get('password')

        user = userRegistration.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        # Clear session
        request.session.pop('reset_email', None)
        request.session.pop('reset_otp', None)

        messages.success(request, "Password reset successful")
        return redirect('userLogin')

    return render(request, 'home/resetPassword.html')

from django.shortcuts import render
from django.db.models import Q
from .models import userRegistration

def coTraveler(request):
    user_id = request.session['id']

    travelers = (
        userRegistration.objects
        .exclude(id=user_id)
        .order_by('registrationDate')[:3]
    )

    return render(request, 'user/coTraveller.html', {'travelers': travelers})

from django.db.models import Exists, OuterRef
from .models import connectedTravelers

from django.db.models import Exists, OuterRef

def profileList(request):
    current_user_id = request.session['id']

    travelers = (
        userRegistration.objects
        .exclude(id=current_user_id)
        .annotate(
            is_connected=Exists(
                connectedTravelers.objects.filter(
                    traveler_id=current_user_id,
                    connected_traveler=OuterRef('pk'),
                    connected_accepted=True
                )
            ),
            is_pending=Exists(
                connectedTravelers.objects.filter(
                    traveler_id=current_user_id,
                    connected_traveler=OuterRef('pk'),
                    connected=True,
                    connected_accepted=False
                )
            )
        )
        .order_by('-registrationDate')   # newest first
    )

    q = request.GET.get('q')
    destination = request.GET.get('destination')
    gender = request.GET.get('gender')

    if q:
        travelers = travelers.filter(Name__icontains=q)

    if destination:
        travelers = travelers.filter(destination=destination)

    if gender:
        travelers = travelers.filter(gender=gender)

    return render(request, 'user/profileList.html', {
        'travelers': travelers
    })

def connect_traveler(request, user_id):
    if request.method == 'POST':
        # logged-in user (sender)
        sender_id = request.session['id']
        sender = get_object_or_404(userRegistration, id=sender_id)

        # user being connected (receiver)
        receiver = get_object_or_404(userRegistration, id=user_id)

        # prevent self-connection
        if sender.id == receiver.id:
            return redirect('coTraveler')

        message = request.POST.get('message', '')

        connection, created = connectedTravelers.objects.get_or_create(
            traveler=sender,
            connected_traveler=receiver,
            defaults={
                'message': message,
                'connected': True
            }
        )

        if not created:
            connection.message = message
            connection.connected = True
            connection.save()

        return redirect('profileDetail', user_id=receiver.id)

    # ✅ fallback response (VERY IMPORTANT)
    return redirect('coTraveler')
def payment(request):
    return render(request,'user/payment.html')
def notification(request):
    user_id = request.session.get('id')
    user = get_object_or_404(userRegistration, id=user_id)

    # requests sent TO this user & not yet accepted
    requests = connectedTravelers.objects.filter(
        connected_traveler=user,
        connected=True,
        connected_accepted=False
    ).select_related('traveler')

    return render(request, 'user/notificationPage.html', {
        'requests': requests
    })


def accept_connection(request, connection_id):
    if request.method == 'POST':
        connection = get_object_or_404(connectedTravelers, id=connection_id)

        connection.connected_accepted = True
        connection.save()

        return redirect('notification')
def cancel_connection(request, user_id):
    if request.method == 'POST':
        sender_id = request.session['id']

        connection = get_object_or_404(
            connectedTravelers,
            traveler_id=sender_id,
            connected_traveler_id=user_id,
            connected_accepted=False
        )

        connection.delete()
        messages.info(request, "Connection request cancelled")

    return redirect('profileDetail', user_id=user_id)
def edit_profile(request):
    user = userRegistration.objects.get(id=request.session['id'])
    return render(request, 'user/edit-Profile.html', {"user": user})


def update_profile(request):
    user = userRegistration.objects.get(id=request.session['id'])

    if request.method == "POST":
        user.Name = request.POST.get("Name")
        user.email = request.POST.get("email")
        user.phoneNumber = request.POST.get("phoneNumber")
        user.gender = request.POST.get("gender")

        age_value = request.POST.get("age")
        user.age = int(age_value) if age_value.strip() != "" else None

        user.bio = request.POST.get("bio")
        user.about = request.POST.get("about")
        user.favDestinations = request.POST.get("favDestinations")
        user.budgetRange = request.POST.get("budgetRange")
        user.travelpreferences = request.POST.get("travelpreferences")
        user.destination = request.POST.get("destination")

        # PROFILE IMAGE UPDATE
        if request.FILES.get("profileImage"):
            user.profileImage = request.FILES.get("profileImage")

        user.save()

        messages.success(request, "Profile Updated Successfully!")
        return redirect("userProfile")

    return redirect("edit_profile")

