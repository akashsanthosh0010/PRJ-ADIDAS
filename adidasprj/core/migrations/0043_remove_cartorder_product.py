# Generated by Django 4.2.7 on 2023-12-06 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_cartorderitems_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorder',
            name='product',
        ),
    ]