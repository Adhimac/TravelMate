from django.db import models

# Create your models here.
class userRegistration(models.Model):
    Name=models.CharField(max_length=38)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=25)
    phoneNumber=models.CharField(max_length=10)

