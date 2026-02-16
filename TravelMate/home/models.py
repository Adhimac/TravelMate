from django.db import models
from datetime import datetime
from django.utils import timezone
from rentalPartner.models import *
from partner.models import *

# Create your models here.
class userRegistration(models.Model):
    Name=models.CharField(max_length=38)
    email=models.EmailField(max_length=50)
    profileImage=models.ImageField(upload_to='userProfile/', null=True, blank=True)
    password=models.CharField(max_length=25)
    phoneNumber=models.CharField(max_length=10)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.IntegerField(max_length=3, null=True, blank=True)
    bio =models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    favDestinations = models.CharField(max_length=100, null=True, blank=True)
    budgetRange = models.CharField(max_length=50, null=True, blank=True)
    travelpreferences = models.CharField(max_length=100, null=True, blank=True)
    registrationDate=models.DateTimeField(default=timezone.now)
    destination=models.CharField(max_length=50, null=True, blank=True)
    connected = models.BooleanField(default=False)
    connected_accepted = models.BooleanField(default=False)


    def __str__(self):
        return self.Name

class bookingDetails(models.Model):
        user = models.ForeignKey(userRegistration, on_delete=models.CASCADE)
        partner = models.ForeignKey(partnerRegistration, on_delete=models.CASCADE)
        car = models.ForeignKey(carDetails, on_delete=models.CASCADE)
        Name = models.CharField(max_length=38)
        phoneNumber = models.CharField(max_length=10)
        pickupLocation = models.CharField(max_length=100)
        dropLocation = models.CharField(max_length=100)
        startDate = models.DateField()
        endDate = models.DateField()
        numberOfDays = models.IntegerField()
        preferredTime = models.TimeField()
        Additionalnotes = models.CharField(max_length=100,null=True, blank=True)
        bookingDate = models.DateTimeField(default=timezone.now)
        paymentMethod = models.BooleanField(default=False)
        confirmStatus = models.BooleanField(default=False)
        bookingStatus = models.BooleanField(default=False)
        carRentPerDay = models.IntegerField()
        carName = models.CharField(max_length=50)
        
class connectedTravelers(models.Model):
    traveler = models.ForeignKey(userRegistration, on_delete=models.CASCADE)
    connected_traveler = models.ForeignKey(userRegistration, related_name='connected_traveler', on_delete=models.CASCADE)
    connectionDate = models.DateTimeField(default=timezone.now)
    connected = models.BooleanField(default=False)
    connected_accepted = models.BooleanField(default=False)
    message = models.CharField(max_length=200, null=True, blank=True)
    reply = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.traveler.Name} connected with {self.connected_traveler.Name}"
class driverBooking(models.Model):
    driver_id = models.ForeignKey(driverRegistration, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(userRegistration, on_delete=models.CASCADE)
    car = models.ForeignKey(carDetails, on_delete=models.CASCADE)
    pickupLocation = models.CharField(max_length=100)
    dropLocation = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    numberOfDays = models.IntegerField()
    preferredTime = models.TimeField()
    bookingDate = models.DateTimeField(default=timezone.now)
    paymentMethod = models.BooleanField(default=False)
    confirmStatus = models.BooleanField(default=False)
    bookingStatus = models.BooleanField(default=False)
    fareperday = models.IntegerField()
    carName = models.CharField(max_length=50)

    def __str__(self):
        return f"Booking by {self.user.Name} with Driver {self.driver.name}"