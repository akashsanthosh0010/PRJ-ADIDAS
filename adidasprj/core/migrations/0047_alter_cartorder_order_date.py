# Generated by Django 4.2.7 on 2023-12-21 16:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0046_alter_cartorder_order_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorder",
            name="order_date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
