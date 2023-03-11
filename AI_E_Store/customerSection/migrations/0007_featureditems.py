# Generated by Django 4.1.3 on 2023-03-11 01:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customerSection', '0006_alter_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedItems',
            fields=[
                ('DateUsed', models.DateField(default=django.utils.timezone.now, primary_key=True, serialize=False)),
                ('Item1', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo1', to='customerSection.iteminstance')),
                ('Item2', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo2', to='customerSection.iteminstance')),
                ('Item3', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo3', to='customerSection.iteminstance')),
                ('Item4', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo4', to='customerSection.iteminstance')),
                ('Item5', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo5', to='customerSection.iteminstance')),
                ('Item6', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo6', to='customerSection.iteminstance')),
                ('Item7', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo7', to='customerSection.iteminstance')),
                ('Item8', models.ForeignKey(db_column='', on_delete=django.db.models.deletion.CASCADE, related_name='ItemNo8', to='customerSection.iteminstance')),
            ],
        ),
    ]
