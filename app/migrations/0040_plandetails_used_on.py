# Generated by Django 5.2.1 on 2025-06-12 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_alter_driverloan_from_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plandetails',
            name='used_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
