# Generated by Django 5.1.6 on 2025-03-20 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0127_aakindia_rate_kg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtrips',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
