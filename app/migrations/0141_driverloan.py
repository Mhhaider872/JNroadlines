# Generated by Django 5.1.6 on 2025-03-25 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0140_expense_actual_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tankerno', models.CharField(max_length=100)),
                ('From_address', models.CharField(max_length=200)),
                ('To_address', models.CharField(max_length=200)),
                ('drivername', models.CharField(max_length=100)),
                ('trip_date', models.DateField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('load', models.IntegerField(blank=True, null=True)),
                ('unload', models.IntegerField(blank=True, null=True)),
                ('short_kg', models.IntegerField(blank=True, null=True)),
                ('allow_kg', models.DecimalField(decimal_places=2, max_digits=5)),
                ('actual_short', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('short_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('previous_loan', models.DecimalField(decimal_places=2, max_digits=5)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
