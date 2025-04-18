# Generated by Django 5.1.6 on 2025-03-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0103_remove_invoice_company_name_invoice_company_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='description',
            new_name='t_add',
        ),
        migrations.AddField(
            model_name='item',
            name='f_add',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='item',
            name='lr_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='tanker_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
