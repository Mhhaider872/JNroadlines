# Generated by Django 5.1.6 on 2025-02-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_plandetails_delete_plans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetails',
            name='area_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='companydetails',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='companydetails',
            name='pincode',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='companydetails',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
