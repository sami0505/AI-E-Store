# Generated by Django 4.1.3 on 2023-01-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerSection', '0006_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='AddressLine2',
            field=models.CharField(max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='County',
            field=models.CharField(max_length=26, null=True),
        ),
    ]
