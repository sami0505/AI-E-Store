# Generated by Django 4.1.3 on 2023-03-07 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerSection', '0012_remove_style_lowresimg_style_highresimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='basket',
            field=models.CharField(default='', max_length=4096),
        ),
        migrations.AddField(
            model_name='customer',
            name='wishlish',
            field=models.CharField(default='', max_length=4096),
        ),
    ]
