# Generated by Django 5.1.6 on 2025-02-21 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FromConsignor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromconsignor', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='ToConsignor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toconsignor', models.CharField(max_length=600)),
            ],
        ),
    ]
