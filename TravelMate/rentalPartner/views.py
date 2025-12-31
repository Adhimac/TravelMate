from django.shortcuts import render,redirect
from .models import *
from home.models import *
from django.contrib import messages

# Create your views here.
def rentalPartnerLogin(request):  
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user=partnerRegistration.objects.get(email=email,password=password)
            request.session['partner_id'] = user.id  # Store partner ID in session
            request.session['partner_name'] = user.name  # Store partner name in session
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
        mobileNumber = request.POST.get("phone") 
        aadharId = request.POST.get("aadhaar")

        if password != confirmPassword:
            messages.error(request, "Passwords do not match")
            return redirect("rentalPartnerRegister")
        if partnerRegistration.objects.filter(email=email).exists():
            messages.error(request, "This email is already in use")
            return redirect("rentalPartnerRegister")
        userdata = partnerRegistration(
            name=name,
            email=email,
            password=(password),
            mobileNumber=mobileNumber,
            aadharId=aadharId,
        )
        userdata.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect("rentalPartnerLogin")
    return render(request,'rentalPartner/rentalPartnerRegister.html')
def rentalPartnerHome(request):   
    return render(request,'rentalPartner/rentalPartnerHome.html')
def addingCars(request):   
    if request.method=="POST":
        vehicleName=request.POST.get("vehicle_name")
        vehicleNumber=request.POST.get("registration_number")
        vehicleType=request.POST.get("vehicle_type")
        seatingCapacity=request.POST.get("seating_capacity")
        rentPerDay=request.POST.get("price_per_day")
        availabilityStatus=request.POST.get("availability")
        vehicleImage=request.FILES.get("vehicleImage")
        partnerId=request.POST.get("partner_id")

        # partner=partnerRegistration.objects.get(id=partnerId)

        car=carDetails(
            vehicleName=vehicleName,
            vehicleNumber=vehicleNumber,
            vehicleType=vehicleType,
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

    # Vehicle type count
    vehicle_counts = (
        carDetails.objects
        .filter(partner_id=partner_id)
        .values('vehicleType')
        .annotate(total=Count('id'))
    )

    # Convert queryset → dict
    vehicle_type_count = {
        item['vehicleType']: item['total']
        for item in vehicle_counts
    }

    context = {
        'vehicle_type_count': vehicle_type_count
    }

    return render(request, 'rentalPartner/rentalPartnerProfile.html', context)

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
