# Generated by Django 4.2.7 on 2023-11-25 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_address_email_address_f_name_address_phone_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone_no',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
