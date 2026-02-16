import re
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.conf import settings
from home.models import *
from django.contrib.auth.hashers import make_password


# Create your views here.
def driverLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            driver = driverRegistration.objects.get(email=email, password=password)

            if driver.status == 'pending':
                messages.warning(request, "Your account is under admin review.")
                return redirect("driverLogin")

            if driver.status == 'rejected':
                messages.error(request, "Your registration was rejected by admin.")
                return redirect("driverLogin")

            request.session['driver_id'] = driver.id
            request.session['driver_name'] = driver.name
            return redirect("driverHome")

        except driverRegistration.DoesNotExist:
            messages.error(request, "Invalid email or password")

    return render(request, 'partner/driverLogin.html')

from django.core.exceptions import ValidationError

def validate_driver_form(request):
    phone = request.POST.get("phoneNumber")
    ifsc = request.POST.get("ifsc")
    password = request.POST.get("password")
    confirm = request.POST.get("confirmPassword")

    if not re.match(r"^[6-9][0-9]{9}$", phone):
        raise ValidationError("Invalid mobile number")

    if not re.match(r"^[A-Z]{4}0[A-Z0-9]{6}$", ifsc):
        raise ValidationError("Invalid IFSC")

    if password != confirm:
        raise ValidationError("Passwords do not match")


def driverRegister(request):
    if request.method == "POST":
        
        try:
            validate_driver_form(request)
        except ValidationError as e:
             messages.error(request, str(e))
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")

        phoneNumber = request.POST.get("phoneNumber")
        location = request.POST.get("location")
        address = request.POST.get("address")
        driver_fee = request.POST.get("driver_fee")

        profileImage = request.FILES.get("profile_image")
        licenceImage = request.FILES.get("license_image")

        licenceNumber = request.POST.get("license_number")
        licenceExpiry = request.POST.get("license_expiry")

        bank_account = request.POST.get("bank_account")
        ifsc = request.POST.get("ifsc")

      

        # PASSWORD CHECK
        if password != confirmPassword:
            messages.error(request, "Passwords do not match")
            return redirect("driverRegister")

        # EMAIL CHECK
        if driverRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("driverRegister")
        if driverRegistration.objects.filter(phoneNumber=phoneNumber).exists():
            messages.error(request, "Phone number already exists")
            return redirect("driverRegister")
        if driverRegistration.objects.filter(licenceNumber=licenceNumber).exists():
            messages.error(request, "Licence number already exists")
            return redirect("driverRegister")

        # SAVE DRIVER
        driver = driverRegistration(
            name=name,
            email=email,
            # password=make_password(password),  # 🔐 HASHED PASSWORD
            password=password,  # 🔐 HASHED PASSWORD
            phoneNumber=phoneNumber,
            location=location,
            address=address,
            driver_fee=driver_fee,

            licenceNumber=licenceNumber,
            licenceExpiry=licenceExpiry,

            bank_account=bank_account,
            ifsc=ifsc,
            status="pending"
        )

        if profileImage:
            driver.profileImage = profileImage
        if licenceImage:
            driver.licenceImage = licenceImage

        driver.save()
        messages.success(request, "Registration submitted. Waiting for admin approval.")
        return redirect("driverLogin")

    return render(request, "partner/driverRegister.html")
def driverHome(request):
    driver_id = request.session.get('driver_id')  # ✅ FIXED
    if not driver_id:
        return redirect('driverLogin')

    driver = driverRegistration.objects.get(id=driver_id)

    return render(request, 'partner/driverHome.html', {
        'driver': driver
    })
def driverBookings(request):
    driver_id = request.session.get('driver_id')  # ✅ FIXED
    if not driver_id:
        return redirect('driverLogin')

    bookings = driverBooking.objects.filter(driver_id=driver_id)
    return render(request, 'partner/driverBookings.html', {'bookings': bookings})

def driverProfile(request):
    driver_id = request.session.get('driver_id')
    if not driver_id:
        return redirect('driverLogin')  
    driver = get_object_or_404(driverRegistration, id=driver_id)
    return render(request,'partner/driverProfile.html',{'driver':driver})

def edit_driver_profile(request):
    driver_id = request.session.get('driver_id')
    if not driver_id:
        return redirect('driverLogin')

    driver = get_object_or_404(driverRegistration, id=driver_id)

    if request.method == 'POST':
        driver.name = request.POST.get('name')
        driver.phoneNumber = request.POST.get('phone')
        driver.city = request.POST.get('city')
        driver.state = request.POST.get('state')
        driver.address = request.POST.get('address')
        driver.licenceType = request.POST.get('vehicle_type')

        # ✅ ONLY update licence number IF provided
        licence_number = request.POST.get('license_number')
        if licence_number:
            driver.licenceNumber = licence_number

        # ✅ Profile image
        if request.FILES.get('profile_image'):
            driver.profileImage = request.FILES['profile_image']

        driver.save()
        return redirect('driverProfile')

    return render(request, 'partner/editProfile.html', {'driver': driver})