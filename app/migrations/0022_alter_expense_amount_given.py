# Generated by Django 5.2.1 on 2025-06-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_items_alter_expense_toll_amount_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount_given',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
