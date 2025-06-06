# Generated by Django 5.2.1 on 2025-05-26 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_tb_invoice_tb_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='VC_Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('company', models.CharField(blank=True, max_length=300, null=True)),
                ('gst', models.CharField(blank=True, max_length=300, null=True)),
                ('pan', models.CharField(blank=True, max_length=300, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_in_words', models.CharField(blank=True, max_length=255)),
                ('tanker', models.CharField(blank=True, max_length=200, null=True)),
                ('From_add', models.CharField(blank=True, max_length=200, null=True)),
                ('To_add', models.CharField(blank=True, max_length=200, null=True)),
                ('date_dis', models.DateField(blank=True, null=True)),
                ('retn', models.IntegerField(blank=True, null=True)),
                ('lr_no', models.CharField(blank=True, max_length=200, null=True)),
                ('sac', models.IntegerField(blank=True, null=True)),
                ('Fo_date', models.DateField(blank=True, null=True)),
                ('To_date', models.DateField(blank=True, null=True)),
                ('d_rate', models.IntegerField(blank=True, null=True)),
                ('par_day', models.IntegerField(blank=True, null=True)),
                ('total_d', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('igst', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('fright_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('hsac', models.IntegerField(blank=True, null=True)),
                ('charges', models.CharField(blank=True, max_length=300, null=True)),
                ('c_gst', models.FloatField(blank=True, default=0.0, null=True)),
                ('s_gst', models.FloatField(blank=True, default=0.0, null=True)),
                ('i_gst', models.FloatField(blank=True, default=0.0, null=True)),
                ('g_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='VC_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app.vc_invoice')),
            ],
        ),
    ]
