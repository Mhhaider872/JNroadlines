# Generated by Django 5.2.1 on 2025-06-17 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_crinvoice_alter_usetool_tool_critem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crinvoice',
            name='date_dis',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
