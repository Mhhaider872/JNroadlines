# Generated by Django 5.2.1 on 2025-06-12 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_remove_usetool_tool_category_usetool_qty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usetool',
            name='tool_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tools'),
        ),
    ]
