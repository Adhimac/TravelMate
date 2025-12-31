from django.db import models
from datetime import datetime
from django.utils import timezone
from rentalPartner.models import *

# Create your models here.
class userRegistration(models.Model):
    Name=models.CharField(max_length=38)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=25)
    phoneNumber=models.CharField(max_length=10)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.IntegerField(max_length=3, null=True, blank=True)
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

        paymentMethod = models.BooleanField(default=False)
        confirmStatus = models.BooleanField(default=False)
        bookingStatus = models.BooleanField(default=False)
        carRentPerDay = models.IntegerField()
        carName = models.CharField(max_length=50)
        