import json
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib import messages

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
            request.session['admin_id'] = admin.id
            return redirect('adminHome')
            # return render(request, 'appadmin/adminHome.html')
        except proAdmin.DoesNotExist:
            error_message = "Invalid username or password."
            return render(request, 'appadmin/adminLogin.html', {'error_message': error_message})  
    return render(request, 'appadmin/adminLogin.html')  

def adminHome(request):
    total_users = userRegistration.objects.count()
    total_drivers = driverRegistration.objects.count()
    total_partners = partnerRegistration.objects.count()
    total_vehicles = carDetails.objects.count()
    total_bookings = bookingDetails.objects.count()

    return render(request, 'appadmin/adminHome.html', {
        'total_users': total_users,
        'total_drivers': total_drivers,
        'total_partners': total_partners,
        'total_vehicles': total_vehicles,
        'total_bookings': total_bookings,
    })
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
    driverBookings = driverBooking.objects.all()
    return render(request, 'appadmin/viewBooking.html', {
        'bookings': bookings,
        'driverBookings': driverBookings
    })
from django.shortcuts import render, redirect, get_object_or_404
from partner.models import driverRegistration



def driverRequests(request):
    drivers = driverRegistration.objects.filter(status='pending')

    # Convert all driver objects to JSON-friendly dictionary
    drivers_json = []
    for d in drivers:
        drivers_json.append({
            "id": d.id,
            "name": d.name,
            "email": d.email,
            "phoneNumber": d.phoneNumber,
            "location": d.location,
            "address": d.address,
            "driver_fee": str(d.driver_fee) if d.driver_fee else None,
            "licenceNumber": d.licenceNumber,
            "licenceExpiry": str(d.licenceExpiry) if d.licenceExpiry else None,
            "licenceImage": d.licenceImage.url if d.licenceImage else "",
            "profileImage": d.profileImage.url if d.profileImage else "",
            # "aadharId": d.aadharId,
            # "aadharImage": d.aadharImage.url if d.aadharImage else "",
            "bank_account": d.bank_account,
            "ifsc": d.ifsc,
            "joinedDate": d.joinedDate.strftime("%Y-%m-%d %H:%M")
        })

    return render(request, "appadmin/driverRequest.html", {
        "drivers": drivers,
        "drivers_json": json.dumps(drivers_json)
    })

def approveDriver(request, driver_id):
    driver = get_object_or_404(driverRegistration, id=driver_id)
    driver.status = 'approved'
    driver.save()
    return redirect('driverRequests')

def rejectDriver(request, driver_id):
    driver = get_object_or_404(driverRegistration, id=driver_id)
    driver.status = 'rejected'
    driver.save()
    return redirect('driverRequests')


# ---------------------------------------------------------
# 1️⃣ RENTAL PARTNER REQUESTS (Full List)
# ---------------------------------------------------------
def rentalPartnerRequests(request):
    partners = partnerRegistration.objects.all()

    # Prepare JSON for View Details modal
    partners_json = []
    for p in partners:
        partners_json.append({
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "mobileNumber": p.mobileNumber,
            "aadharId": p.aadharId,
            "combanyName": p.combanyName,
            "location": p.location,
            "GST_number": p.GST_number,
            "status": p.status,
            "verified": p.verified,
            "city": p.city,
            "state": p.state,
            "Address": p.Address,
            "profileImage": p.profileImage.url if p.profileImage else "",
            "aadharImage": p.aadharImage.url if p.aadharImage else "",
            "shopImage": p.shopImage.url if p.shopImage else "",
        })

    return render(
        request,
        "appadmin/rentalPartnerRequests.html",
        {
            "partners": partners,
            "partners_json": json.dumps(partners_json)
        }
    )


# ---------------------------------------------------------
# 2️⃣ APPROVE RENTAL PARTNERS PAGE (Only Pending)
# ---------------------------------------------------------
def approveRentalPartners(request):
    partners = partnerRegistration.objects.filter(status='pending')

    partners_json = []
    for p in partners:
        partners_json.append({
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "mobileNumber": p.mobileNumber,
            "aadharId": p.aadharId,
            "combanyName": p.combanyName,
            "location": p.location,
            "GST_number": p.GST_number,
            "status": p.status,
            "verified": p.verified,
            "city": p.city,
            "state": p.state,
            "Address": p.Address,
            "profileImage": p.profileImage.url if p.profileImage else "",
            "aadharImage": p.aadharImage.url if p.aadharImage else "",
            "shopImage": p.shopImage.url if p.shopImage else "",
        })

    return render(
        request,
        "appadmin/approve_rental_partners.html",
        {"partners": partners, "partners_json": json.dumps(partners_json)}
    )


# ---------------------------------------------------------
# 3️⃣ APPROVE ACTION
# ---------------------------------------------------------
def approvePartner(request, id):
    partner = get_object_or_404(partnerRegistration, id=id)
    partner.status = 'approved'
    partner.save()

    messages.success(request, "Rental Partner approved successfully")
    return redirect('approveRentalPartners')


# ---------------------------------------------------------
# 4️⃣ REJECT ACTION
# ---------------------------------------------------------
def rejectPartner(request, id):
    partner = get_object_or_404(partnerRegistration, id=id)
    partner.status = 'rejected'
    partner.save()

    messages.success(request, "Rental Partner rejected successfully")
    return redirect('approveRentalPartners')

def adminPartnerManagement(request):
    partners = partnerRegistration.objects.all()
    return render(request, 'appadmin/adminPartnerManagement.html', {'partners': partners})
def rentalPartnerManagement(request):
    # Fetch all partners (you can add ordering if needed)
    partners = partnerRegistration.objects.all().order_by('-id')

    return render(request, 'appadmin/adminPartnerManagement.html', {
        'partners': partners
    })