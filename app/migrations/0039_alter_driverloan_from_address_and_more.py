# Generated by Django 5.2.1 on 2025-06-07 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_alter_driverloan_date_alter_driverloan_trip_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverloan',
            name='From_address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='driverloan',
            name='To_address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='driverloan',
            name='drivername',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
