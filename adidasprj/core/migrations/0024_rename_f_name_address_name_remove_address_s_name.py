# Generated by Django 4.2.7 on 2023-11-25 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_address_city_address_landmark'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='f_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='address',
            name='s_name',
        ),
    ]