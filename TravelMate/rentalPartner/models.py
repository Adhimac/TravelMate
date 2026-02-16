from django.db import models

# Create your models here.
class partnerRegistration(models.Model):
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=25)
    mobileNumber = models.IntegerField()
    aadharId = models.IntegerField()
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    combanyName = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    GST_number = models.CharField(max_length=15, null=True, blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # 📄 NEW FIELDS
    aadharImage = models.ImageField(
        upload_to='partner_documents/aadhar/',
        null=True,
        blank=True
    )
    shopImage = models.ImageField(
        upload_to='partner_documents/shop/',
        null=True,
        blank=True
    )
    verified = models.BooleanField(default=False)


    # city = models.CharField(max_length=50, null=True, blank=True)
    # state = models.CharField(max_length=50, null=True, blank=True)
    Address = models.TextField(null=True, blank=True)

    profileImage = models.ImageField(
        upload_to='partner_images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class carDetails(models.Model):
    vehicleName=models.CharField(max_length=50)
    vehicleNumber=models.CharField(max_length=15)   
    vehicleType=models.CharField(max_length=20)
    fuelType=models.CharField(max_length=20, null=True, blank=True)
    seatingCapacity=models.IntegerField()
    rentPerDay=models.IntegerField()
    availabilityStatus=models.BooleanField(default=True)
    partner=models.ForeignKey(partnerRegistration,on_delete=models.CASCADE)
    vehicleImage=models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    def __str__(self):
        return self.vehicleName                                                                                                                         
