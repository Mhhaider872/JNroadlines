# Generated by Django 5.2.1 on 2025-06-12 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_alter_tools_tool_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usetool',
            name='tool_category',
        ),
        migrations.AddField(
            model_name='usetool',
            name='qty',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
