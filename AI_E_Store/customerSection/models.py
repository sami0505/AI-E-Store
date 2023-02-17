from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone


# The Customer is the default user model, capable of ordering items, logging in etc.
class Customer(AbstractBaseUser, PermissionsMixin):
    CustomerID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16, blank=False, unique=True)  # **
    Firstname = models.CharField(max_length=32, blank=False)
    Surname = models.CharField(max_length=32, blank=False)
    email = models.EmailField(max_length=64, blank=False)  # **
    Telephone = models.CharField(max_length=32, blank=False)
    Title = models.CharField(max_length=4, blank=False)
    DateOfBirth = models.DateField(blank=False)
    date_joined = models.DateTimeField(blank=False, default=timezone.now)  # **
    is_staff = models.BooleanField(default=False)  # **
    is_active = models.BooleanField(default=False)  # **
    is_superuser = models.BooleanField(default=False)  # **
    objects = UserManager()
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["Firstname", "Surname", "Email", "Telephone",
                       "Title", "DateOfBirth", "DateJoined"]
    # **Lowercase to keep default UserManager working


# The Item model contains generic item info that can be applied to all instances of it
class Item(models.Model):
    ItemID = models.AutoField(primary_key=True, blank=False)
    Title = models.CharField(max_length=32, blank=False)
    Description = models.CharField(max_length=256, blank=False)
    Price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    Category = models.CharField(max_length=20, blank=False)


# The ItemInstance model contains the highly specific info per "style" of an item. Blue, Red, Small, Big etc
class ItemInstance(models.Model):
    ItemInstanceID = models.AutoField(primary_key=True, blank=False)
    ItemID = models.ForeignKey("Item", on_delete=models.CASCADE, db_column="", blank=False)
    Size = models.CharField(max_length=3, blank=False)
    Colour = models.CharField(max_length=16, blank=False)
    Quantity = models.SmallIntegerField(blank=False)
    AmountSold = models.IntegerField(blank=False)
    IsPublic = models.BooleanField(blank=False)
    HighResImg = models.ImageField(width_field=1080, height_field=1080, blank=False)
    LowResImg = models.ImageField(width_field=256, height_field=256, blank=False)
    QBR = models.DecimalField(default=-1.0, max_digits=3, decimal_places=2, blank=False)


# The Review model is a singular record of a user's review
class Review(models.Model):
    ReviewID = models.AutoField(primary_key=True, blank=False)
    CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE, db_column="", blank=False)
    ItemID = models.ForeignKey("Item", on_delete=models.CASCADE, db_column="", blank=False)
    Comment = models.CharField(max_length=256, blank=False)
    StarRating = models.SmallIntegerField(blank=False)


# The Order model contains the bulk of information for an order, without the items
class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE, db_column="", blank=False)
    DateOfSale = models.DateField(blank=False)
    PaymentMethod = models.CharField(max_length=32, blank=False)
    IsShipped = models.BooleanField(default=False, blank=False)
    Postcode = models.CharField(max_length=7, blank=False)
    AddressLine1 = models.CharField(max_length=35, blank=False)
    AddressLine2 = models.CharField(max_length=35, null=True)
    City = models.CharField(max_length=26, blank=False)
    County = models.CharField(max_length=26, null=True)


# The OrderLine model is used to record each item ordered per Order
class OrderLine(models.Model):
    OrderLineID = models.AutoField(primary_key=True, blank=False)
    ItemInstanceID = models.ForeignKey("ItemInstance", on_delete=models.CASCADE, db_column="", blank=False)
    Quantity = models.SmallIntegerField(blank=False)
