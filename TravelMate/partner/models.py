from django.db import models
from django.utils import timezone


class driverRegistration(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    # Personal Details
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    
    location = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    driver_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Licence
    licenceNumber = models.CharField(max_length=30)
    licenceExpiry = models.DateField(null=True, blank=True)
    licenceImage = models.ImageField(upload_to='driver_licences/', null=True, blank=True)

    # Documents
    profileImage = models.ImageField(upload_to='driver_profiles/', null=True, blank=True)
    # aadharId = models.CharField(max_length=12)
    # aadharImage = models.ImageField(upload_to='driver_aadhars/', null=True, blank=True)

    # Bank
    bank_account = models.CharField(max_length=50, null=True, blank=True)
    ifsc = models.CharField(max_length=20, null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    joinedDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.status})"