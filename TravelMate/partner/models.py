from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class driverRegistration(models.Model):
    name=models.CharField(max_length=25)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=25)
    licenceNumber=models.CharField(max_length=25)
    location=models.CharField(max_length=50, null=True, blank=True)
    aadharId=models.IntegerField(max_length=12)
    phoneNumber=models.IntegerField(max_length=10, null=True, blank=True)
    address=models.CharField(max_length=100, null=True, blank=True)
    profileImage=models.ImageField(upload_to='driver_profiles/', null=True, blank=True)
    licenceImage=models.ImageField(upload_to='driver_licences/', null=True, blank=True)
    licenceType=models.CharField(max_length=20, null=True, blank=True)
    driverJoinedDate=models.DateField(default=timezone.now)
    def __str__(self):
        return self.name
