# Generated by Django 5.1.6 on 2025-03-25 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0152_alter_driverloan_allow_kg_alter_driverloan_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverloan',
            name='short_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
