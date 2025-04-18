# Generated by Django 5.1.6 on 2025-03-01 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_diesel_detail_delete_dieseldetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_name', models.CharField(max_length=200)),
                ('owner_name', models.CharField(max_length=200)),
                ('making_year', models.DateField(null=True)),
                ('chassise_no', models.CharField(max_length=200)),
                ('engine_no', models.CharField(max_length=200)),
                ('insurance_date', models.DateField(null=True)),
                ('state_permit', models.DateField(null=True)),
                ('national_permit', models.DateField(null=True)),
                ('fitness_date', models.DateField(null=True)),
                ('tax_date', models.DateField(null=True)),
                ('puc_date', models.DateField(null=True)),
                ('vehicle_img', models.FileField(upload_to='vehicle_image/')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('toll_name', models.CharField(max_length=200)),
                ('From_address', models.CharField(max_length=200)),
                ('To_address', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='newdriverdetails',
            name='img',
        ),
        migrations.AlterField(
            model_name='newdriverdetails',
            name='imguploads',
            field=models.FileField(upload_to='pdfs/'),
        ),
        migrations.DeleteModel(
            name='OwnerName',
        ),
        migrations.DeleteModel(
            name='TruckNo',
        ),
    ]
