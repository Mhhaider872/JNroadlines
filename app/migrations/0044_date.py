# Generated by Django 5.1.6 on 2025-03-04 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_alter_all_trip_tdate_alter_all_trip_tripdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
    ]
