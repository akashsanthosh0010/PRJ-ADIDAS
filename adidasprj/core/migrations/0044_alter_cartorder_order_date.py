# Generated by Django 4.2.7 on 2023-12-08 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_remove_cartorder_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
