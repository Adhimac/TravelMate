from urllib import request
from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from home.models import *
from django.contrib import messages

# Create your views here.
def rentalPartnerLogin(request):  
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = partnerRegistration.objects.get(email=email, password=password)

            # 🔒 ADMIN APPROVAL CHECK
            if not user.status == 'approved':
                messages.error(
                    request,
                    "Your account is not approved yet. Please wait for admin approval."
                )
                return redirect("rentalPartnerLogin")

            request.session['partner_id'] = user.id
            request.session['partner_name'] = user.name

            messages.success(request, "Login successful.")
            return redirect("rentalPartnerHome")

        except partnerRegistration.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("rentalPartnerLogin")

    return render(request,'rentalPartner/rentalPartnerLogin.html')
 
def rentalPartnerRegister(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirm_password")
        mobileNumber = request.POST.get("mobileNumber")
        aadharId = request.POST.get("aadharId")
        combanyName = request.POST.get("combanyName")
        GST_number = request.POST.get("GST_number")
        city = request.POST.get("city")
        state = request.POST.get("state")
        Address = request.POST.get("Address")

        location = request.POST.get("location")
       
        aadharImage = request.FILES.get("aadharImage")
        shopImage = request.FILES.get("shopImage")

        # password validation
        if password != confirmPassword:
            messages.error(request, "Passwords do not match")
            return redirect("rentalPartnerRegister")

        # Create partner
        partnerRegistration.objects.create(
            name=name,
            email=email,
            password=password,
            location=location,
            city=city,
            state=state,
            combanyName=combanyName,
            mobileNumber=mobileNumber,
            aadharId=aadharId,
            aadharImage=aadharImage,
            shopImage=shopImage,
            verified=False,  # ✔ now allowed
            status="pending",  # admin must approve
            GST_number=GST_number,
            Address=Address
        )

        messages.success(request, "Registration submitted. Awaiting admin verification.")
        return redirect("rentalPartnerLogin")

    return render(request, "rentalPartner/rentalPartnerRegister.html")



def rentalPartnerHome(request):   
    pro = partnerRegistration.objects.get(id=request.session['partner_id'])
    return render(request,'rentalPartner/rentalPartnerHome.html' ,{'pro':pro})
def addingCars(request):   
    if request.method=="POST":
        vehicleName=request.POST.get("vehicle_name")
        vehicleNumber=request.POST.get("registration_number")
        vehicleType=request.POST.get("vehicle_type")
        fuelType=request.POST.get("fuel_type")
        seatingCapacity=request.POST.get("seating_capacity")
        rentPerDay=request.POST.get("price_per_day")
        availabilityStatus=request.POST.get("availability")
        vehicleImage=request.FILES.get("vehicle_images")
        # partnerId=request.POST.get("partner_id")

        # partner=partnerRegistration.objects.get(id=partnerId)
        car=carDetails(
            vehicleName=vehicleName,
            vehicleNumber=vehicleNumber,
            vehicleType=vehicleType,
            fuelType=fuelType,
            seatingCapacity=seatingCapacity,
            rentPerDay=rentPerDay,
            partner_id=request.session['partner_id'],
            vehicleImage=vehicleImage,
            availabilityStatus=availabilityStatus
        )
        car.save()
        messages.success(request, "Car added successfully.")
        return redirect("addingCars")   
    return render(request,'rentalPartner/addingCars.html')
# def rentalPartnerProfile(request):   
#     return render(request,'rentalPartner/rentalPartnerProfile.html')
from django.db.models import Count
# from .models import carDetails

def rentalPartnerProfile(request):
    partner_id = request.session.get('partner_id')

    if not partner_id:
        return redirect('partnerLogin')  # safety check

    # 🔹 Fetch partner
    pro = partnerRegistration.objects.get(id=partner_id)

    # 🔹 HANDLE POPUP FORM SUBMIT
    if request.method == "POST":
        # Profile / Owner details
        pro.image = request.FILES.get('imageprofileImage') 
        pro.name = request.POST.get('name')
        pro.email = request.POST.get('email')
        pro.mobileNumber = request.POST.get('mobileNumber')

        # Business details
        pro.aadharId = request.POST.get('aadharId')
        pro.combanyName = request.POST.get('combanyName')
        pro.city = request.POST.get('city')
        pro.state = request.POST.get('state')
        pro.Address = request.POST.get('address')
        pro.GST_number = request.POST.get('GST_number')

        pro.save()

        messages.success(request, "Profile updated successfully")
        return redirect('rentalPartnerProfile')

    # 🔹 VEHICLE TYPE COUNT
    vehicle_counts = (
        carDetails.objects
        .filter(partner_id=partner_id)
        .values('vehicleType')
        .annotate(total=Count('id'))
    )

    vehicle_type_count = {
        item['vehicleType']: item['total']
        for item in vehicle_counts
    }

    context = {
        'pro': pro,
        'vehicle_type_count': vehicle_type_count
    }

    return render(
        request,
        'rentalPartner/rentalPartnerProfile.html',
        context
    )

def rentalPartnerBookings(request):
    # Get logged-in partner id from session
    partner_id = request.session.get('partner_id')

    # Fetch bookings related to this partner's vehicles
    bookings = bookingDetails.objects.filter(
        car__partner_id=partner_id
    ).select_related('car')

    # Context dictionary
    context = {
        'bookings': bookings
    }

    return render(request, 'rentalPartner/rentalPartnerViewBooking.html', context)

def myCars(request):
    partner_id = request.session.get('partner_id')

    cars = carDetails.objects.filter(partner_id=partner_id)

    context = {
        'cars': cars
    }

    return render(request, 'rentalPartner/myCars.html', context)
def editCar(request, car_id):
    partner_id = request.session.get('partner_id')
    partner = get_object_or_404(partnerRegistration, id=partner_id)

    # ✅ Security: partner can edit ONLY their own car
    car = get_object_or_404(carDetails, id=car_id, partner=partner)

    if request.method == "POST":
        car.vehicleName = request.POST.get('vehicleName')
        car.vehicleType = request.POST.get('vehicleType')
        car.vehicleNumber = request.POST.get('vehicleNumber')
        car.fuelType = request.POST.get('fuelType')
        car.seatingCapacity = request.POST.get('seatingCapacity')
        car.rentPerDay = request.POST.get('rentPerDay')
        car.availabilityStatus = request.POST.get('availabilityStatus') == 'on'

        if 'vehicleImage' in request.FILES:
            car.vehicleImage = request.FILES['vehicleImage']

        car.save()
        messages.success(request, "Car details updated successfully")

        return redirect('myCars')
    context = {
        'car': car      
    }
    return render(request, 'rentalPartner/editCar.html', context)   

def deleteCar(request, id):
    car = get_object_or_404(carDetails, id=id)
    car.delete()
    return redirect('myCars')