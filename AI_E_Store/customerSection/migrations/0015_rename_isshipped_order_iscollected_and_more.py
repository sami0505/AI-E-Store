# Generated by Django 4.1.3 on 2023-03-12 19:38

import customerSection.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerSection', '0014_rename_wishlish_customer_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='IsShipped',
            new_name='IsCollected',
        ),
        migrations.RemoveField(
            model_name='order',
            name='AddressLine1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='AddressLine2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='City',
        ),
        migrations.RemoveField(
            model_name='order',
            name='County',
        ),
        migrations.RemoveField(
            model_name='order',
            name='DateOfSale',
        ),
        migrations.RemoveField(
            model_name='order',
            name='Postcode',
        ),
        migrations.AddField(
            model_name='order',
            name='DateOfPlacement',
            field=models.DateField(default=customerSection.models.today),
        ),
        migrations.AlterField(
            model_name='order',
            name='PaymentMethod',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
