from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Item, Style, Review, Order, OrderLine, TokenAction


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('ItemID', 'Title', 'Description', 'Price', 'Category')


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('StyleID', 'ItemID', 'Size', 'Colour', 'Quantity',
                    'AmountSold', 'IsPublic', 'QBR')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('OrderID', 'CustomerID', 'PaymentMethod', "IsCollected")


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('OrderLineID', 'OrderID', 'StyleID', 'Quantity')


    # list_display = ('StyleID', 'ItemID', 'Size', 'Colour', 'Quantity',
    #                 'AmountSold', 'IsPublic', 'HighResImg', 'LowResImg', 'QBR')


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('ReviewID', 'CustomerID', 'ItemID', 'Comment', 'StarRating')


# @admin.register(TokenAction)
# class TokenActionAdmin(admin.ModelAdmin):
#     list_display = ('Token', 'Reason', 'Action')


# @admin.register(Customer)
# class CustomerAdmin(UserAdmin):
#     list_display = ('CustomerID', 'username', 'email', 'Firstname', 'Surname',
#                     'Telephone', 'Title', 'DateOfBirth', 'date_joined',
#                     'is_staff', 'is_active', 'is_superuser')