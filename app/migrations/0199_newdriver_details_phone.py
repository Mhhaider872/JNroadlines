# Generated by Django 5.1.6 on 2025-04-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0198_remove_plandetails_drivername_plandetails_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='newdriver_details',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
