# Generated by Django 4.1.3 on 2023-02-25 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerSection', '0008_remove_style_highresimg_remove_style_lowresimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='AddressLine2',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='County',
            field=models.CharField(blank=True, max_length=26, null=True),
        ),
    ]
