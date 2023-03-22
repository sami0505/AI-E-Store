# Administration File
from django.contrib import admin
from .models import Item, Style, Order, OrderLine

admin.site.site_title = "Nick&Zayne"
admin.site.site_header = "Nick&Zayne"
admin.site.index_title = "Management Section"


# Show the Items
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('ItemID', 'Title', 'Description', 'Price', 'Category')


# Show the Styles
@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('StyleID', 'ItemID', 'Size', 'Colour', 'Quantity',
                    'AmountSold', 'IsPublic', 'QBR')


# Show the Orders
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('OrderID', 'CustomerID', 'PaymentMethod', "IsCollected", "totalPrice")
    
    # Display the total price of the order
    def totalPrice(self, obj):
        return obj.getTotalPrice()
    totalPrice.short_description = 'Total Cost'


# Show the OrderLines
@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('OrderLineID', 'OrderID', 'StyleID', 'Quantity')
