# Generated by Django 5.1.6 on 2025-03-06 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_remove_trip_expense_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip_expense',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
