# Generated by Django 5.1.6 on 2025-03-21 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0132_expense_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddBank_Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
