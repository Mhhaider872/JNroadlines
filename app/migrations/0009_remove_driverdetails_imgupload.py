# Generated by Django 5.1.6 on 2025-02-24 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_newdriverdetails_delete_pdfupload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverdetails',
            name='imgupload',
        ),
    ]
