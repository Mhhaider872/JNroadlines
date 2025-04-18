# Generated by Django 5.1.6 on 2025-03-19 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0123_remove_cargill_m_bill_delete_bill_delete_cargill_m'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('company', models.CharField(max_length=255)),
                ('gst', models.CharField(max_length=255)),
                ('pan', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TankerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanker', models.CharField(max_length=255)),
                ('from_address', models.CharField(max_length=255)),
                ('to_address', models.CharField(max_length=255)),
                ('dispatch_date', models.DateField()),
                ('tanker_capacity', models.IntegerField()),
                ('lr_num', models.IntegerField()),
                ('loaded_qty', models.IntegerField()),
                ('rate_per_kg', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tanker_details', to='app.bill')),
            ],
        ),
    ]
