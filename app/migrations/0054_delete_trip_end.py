# Generated by Django 5.1.6 on 2025-03-05 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_remove_trip_tanker_alter_trip_end_amount_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Trip_End',
        ),
    ]
