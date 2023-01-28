from django.db import models

# Create your models here.

class Customer(models.Model):
    Firstname = models.CharField(max_length=32)
    Surname = models.CharField(max_length=32)
    Email = models.EmailField(max_length=64)
    Telephone = models.CharField(max_length=32)
    Username = models.CharField(max_length=16)
    Password = models.CharField(max_length=60)
    Title = models.CharField(max_length=4)
    DateOfBirth = models.DateField()
    DateJoined = models.DateField()
    IsActivated = models.BooleanField()