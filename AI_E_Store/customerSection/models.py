from django.db import models

# Create your models here.

class Customer(models.Model):
    CustomerID = models.AutoField(primary_key=True)
    Firstname = models.CharField(max_length=32)
    Surname = models.CharField(max_length=32)
    Email = models.EmailField(max_length=64)
    Telephone = models.CharField(max_length=32)
    Username = models.CharField(max_length=16)
    Password = models.CharField(max_length=60)
    Title = models.CharField(max_length=4)
    DateOfBirth = models.DateField()
    DateJoined = models.DateField()
    IsActivated = models.BooleanField(default=False)

class Item(models.Model):
    ItemID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=32)
    Description = models.CharField(max_length=256)
    Price = models.DecimalField(max_digits=6, decimal_places=2)
    Category = models.CharField(max_length=20)

class ItemInstance(models.Model):
    ItemInstanceID = models.AutoField(primary_key=True)
    ItemID = models.ForeignKey("Item", on_delete=models.CASCADE, db_column="")
    Size = models.CharField(max_length=3)
    Colour = models.CharField(max_length=16)
    Quantity = models.SmallIntegerField()
    AmountSold = models.IntegerField()
    IsPublic = models.BooleanField()
    HighResImg = models.ImageField(width_field=1080, height_field=1080)
    LowResImg = models.ImageField(width_field=256, height_field=256)
    QBR = models.DecimalField(max_digits=3, decimal_places=2)

class Review(models.Model):
    ReviewID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE, db_column="")
    ItemID = models.ForeignKey("Item", on_delete=models.CASCADE, db_column="")
    Comment = models.CharField(max_length=256)
    StarRating = models.SmallIntegerField()

class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE, db_column="")
    DateOfSale = models.DateField()
    PaymentMethod = models.CharField(max_length=32)
    IsShipped = models.BooleanField(default=False)
    Postcode = models.CharField(max_length=7)
    AddressLine1 = models.CharField(max_length=35)
    AddressLine2 = models.CharField(max_length=35, null=True)
    City = models.CharField(max_length=26)
    County = models.CharField(max_length=26, null=True)

class OrderLine(models.Model):
    OrderLineID = models.AutoField(primary_key=True)
    ItemInstanceID = models.ForeignKey("ItemInstance", on_delete=models.CASCADE, db_column="")
    Quantity = models.SmallIntegerField