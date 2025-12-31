from django.db import models

# Create your models here.
class proAdmin(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username    
    