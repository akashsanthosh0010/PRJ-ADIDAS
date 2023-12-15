# Generated by Django 4.2.7 on 2023-11-21 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_productattribute_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='old_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=9999999999),
            preserve_default=False,
        ),
    ]