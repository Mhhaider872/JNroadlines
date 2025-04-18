# Generated by Django 5.1.6 on 2025-03-25 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0148_alter_driverloan_loan_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverloan',
            name='actual_short',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='driverloan',
            name='loan_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='driverloan',
            name='previous_loan',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='driverloan',
            name='rate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='driverloan',
            name='short_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
