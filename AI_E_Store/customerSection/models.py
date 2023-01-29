from django.db import models

# Create your models here.

class Customer(models.Model):
    CustomerID = models.IntegerField(primary_key=True)
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

class Item(models.Model):
    ItemID = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=32)
    Description = models.CharField(max_length=256)
    Price = models.DecimalField(max_digits=6, decimal_places=2)
    Category = models.CharField(max_length=20)

class Review(models.Model):
    ReviewID = models.IntegerField(primary_key=True)
    CustomerID = models.ForeignKey('Customer', on_delete=models.CASCADE)
    ItemID = models.ForeignKey('Item', on_delete=models.CASCADE)
    Comment = models.CharField(max_length=256)
    StarRating = models.IntegerField()