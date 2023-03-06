from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, Item, Style, Review, Order, OrderLine, TokenAction


# @admin.register(Customer)
# class CustomerAdmin(UserAdmin):
#     list_display = ('CustomerID', 'username', 'email', 'Firstname', 'Surname',
#                     'Telephone', 'Title', 'DateOfBirth', 'date_joined',
#                     'is_staff', 'is_active', 'is_superuser')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('ItemID', 'Title', 'Description', 'Price', 'Category')


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('StyleID', 'ItemID', 'Size', 'Colour', 'Quantity',
                    'AmountSold', 'IsPublic', 'QBR')
    # list_display = ('StyleID', 'ItemID', 'Size', 'Colour', 'Quantity',
    #                 'AmountSold', 'IsPublic', 'HighResImg', 'LowResImg', 'QBR')


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('ReviewID', 'CustomerID', 'ItemID', 'Comment', 'StarRating')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('OrderID', 'CustomerID', 'DateOfSale', 'PaymentMethod',
                    'IsShipped', 'Postcode', 'AddressLine1', 'AddressLine2', 'City', 'County')


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('OrderLineID', 'OrderID', 'StyleID', 'Quantity')


# @admin.register(TokenAction)
# class TokenActionAdmin(admin.ModelAdmin):
#     list_display = ('Token', 'Reason', 'Action')
