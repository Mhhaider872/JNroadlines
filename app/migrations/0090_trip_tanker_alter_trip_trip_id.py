# Generated by Django 5.1.6 on 2025-03-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0089_alter_trip_trip_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='tanker',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='trip_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
