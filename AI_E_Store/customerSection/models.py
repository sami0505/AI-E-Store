from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files import File
import urllib
import os
from PIL import Image
import random
import string


# The Customer is the default user model, capable of ordering items, logging in etc.
class Customer(AbstractBaseUser, PermissionsMixin):
    CustomerID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=16, blank=False, unique=True)  # **
    Firstname = models.CharField(max_length=32, blank=False)
    Surname = models.CharField(max_length=32, blank=False)
    email = models.EmailField(max_length=64, blank=False, unique=True)  # **
    Telephone = models.CharField(max_length=32, blank=False)
    Title = models.CharField(max_length=4, blank=False)
    DateOfBirth = models.DateField(blank=False)
    date_joined = models.DateTimeField(blank=False, default=timezone.now)  # **
    basket = models.CharField(max_length=4096, default="")
    wishlist = models.CharField(max_length=4096, default="")
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

    # This method returns the styles of this ItemID
    def getStyles(self):
        styles = Style.objects.all().filter(ItemID=self)
        return styles
    
    # This method returns the mean star rating of an item over all its reviews
    def getMeanRating(self):
        reviews = Review.objects.filter(ItemID=self.ItemID)
        if len(reviews) > 0:
            sum = 0
            for review in reviews:
                sum += review.StarRating
            mean = sum // len(reviews)
            return mean
        else:
            return 0
        

# The Style model contains the highly specific info per "style" of an item. Blue, Red, Small, Big etc
class Style(models.Model):
    StyleID = models.AutoField(primary_key=True, blank=False)
    ItemID = models.ForeignKey("Item", on_delete=models.CASCADE, db_column="", blank=False)
    Size = models.CharField(max_length=3, blank=False)
    Colour = models.CharField(max_length=16, blank=False)
    Quantity = models.SmallIntegerField(blank=False)
    AmountSold = models.IntegerField(blank=False, default=0)
    IsPublic = models.BooleanField(blank=False)
    HighResImg = models.ImageField()
    QBR = models.DecimalField(default=-1.0, max_digits=3, decimal_places=2, blank=False)


# This model contains a recorded "generation" of the featured items
class FeaturedItems(models.Model):
    DateUsed = models.DateField(primary_key=True, default=timezone.now().date)
    Item1 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo1")
    Item2 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo2")
    Item3 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo3")
    Item4 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo4")
    Item5 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo5")
    Item6 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo6")
    Item7 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo7")
    Item8 = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False, related_name="ItemNo8")

    # This function writes the items of the given list to the fields of this generation of featured
    def writeItems(self, itemsGiven):
        if len(itemsGiven) == 8:
            self.Item1=itemsGiven[0]
            self.Item2=itemsGiven[1]
            self.Item3=itemsGiven[2]
            self.Item4=itemsGiven[3]
            self.Item5=itemsGiven[4]
            self.Item6=itemsGiven[5]
            self.Item7=itemsGiven[6]
            self.Item8=itemsGiven[7]
        else:
            raise Exception("The list given for the items written is of an incorrect length.")

    # This function returns the items of the current featured items
    def returnItems(self):
        itemList = []
        itemList.append(self.Item1)
        itemList.append(self.Item2)
        itemList.append(self.Item3)
        itemList.append(self.Item4)
        itemList.append(self.Item5)
        itemList.append(self.Item6)
        itemList.append(self.Item7)
        itemList.append(self.Item8)
        return itemList


# The Review model is a singular record of a user's review
class Review(models.Model):
    ReviewID = models.AutoField(primary_key=True, blank=False)
    CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE, db_column="", blank=False)
    ItemID = models.ForeignKey("Item", on_delete=models.CASCADE, db_column="", blank=False)
    Comment = models.CharField(max_length=256, blank=False)
    StarRating = models.SmallIntegerField(blank=False)


# This function was needed to make defaulting with timezone.now().date possible
def today():
    date = timezone.now().date()
    return date

# The Order model contains the bulk of information for an order, without the items
class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    CustomerID = models.ForeignKey("Customer", on_delete=models.CASCADE, db_column="", blank=False)
    DateOfPlacement = models.DateField(blank=False, default=today)
    PaymentMethod = models.CharField(max_length=32, blank=True, null=True)
    IsCollected = models.BooleanField(default=False, blank=False)

    # This function returns the total payment of an order. This allows for easy display.
    def getTotalPrice(self):
        orderLines = OrderLine.objects.filter(OrderID=self)
        totalPrice = 0
        for orderLine in orderLines:
            style = orderLine.StyleID
            itemPrice = style.ItemID.Price
            totalPrice += itemPrice * orderLine.Quantity
        return totalPrice


# The OrderLine model is used to record each item ordered per Order
class OrderLine(models.Model):
    OrderLineID = models.AutoField(primary_key=True, blank=False)
    OrderID = models.ForeignKey("Order", on_delete=models.CASCADE, db_column="", blank=False)
    StyleID = models.ForeignKey("Style", on_delete=models.CASCADE, db_column="", blank=False)
    Quantity = models.SmallIntegerField(blank=False)


# This function is used to generate a random token for TokenAction
def generateToken():
    charset = string.ascii_letters  # Use random ASCII letters
    while True:  # Keeps generating random tokens until..
        token = ''.join(random.choice(charset) for i in range(15))
        try:
            TokenAction.objects.get(pk=token)  # get() will return an error if the token is unique
        except ObjectDoesNotExist:
            break  # The loop breaks because it is a unique token
    return token

# The TokenAction model contains a record between a token and what action should follow
class TokenAction(models.Model):
    Token = models.CharField(primary_key=True, max_length=15, default=generateToken)
    Reason = models.PositiveSmallIntegerField(blank=False)  # The reason field generates the action
    Action = models.CharField(max_length=255, blank=False)

    # create() is TokenAction's constructor. Based on reason's value, an action is made according to the userid
    @classmethod
    def create(cls, reason, userid):
        """ Reasons:
            0: Account Creation
            1: Password Reset
            2: Account Deletion """
        if reason == 0:  # Account Creation
            action = f"Customer.objects.filter(CustomerID={userid}).update(is_active=True)"
        elif reason == 1:  # Password Reset
            action = f"c=Customer.objects.get(pk={userid});c.set_password"
        elif reason == 2:  # Account Deletion
            action = f"Customer.objects.get(pk={userid}).delete()"
        else:  # Invalid reason
            raise Exception("Error: Invalid reason value given!")
        return cls(Reason=reason, Action=action)  # The model is created and returned

    # This function returns the url with the given token
    def getURL(self):
        return f"http://127.0.0.1:8000/verification/{self.Token}/"

    def getResetUserID(self):
        # The userID can be acquired by removing the sides of the action
        if self.Reason == 1:
            userID = self.Action[26:-16]
            return int(userID)
        else:  # Wrong reason
            return -1