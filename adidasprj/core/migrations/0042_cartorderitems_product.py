# Generated by Django 4.2.7 on 2023-12-06 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_cartorder_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorderitems',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.product'),
            preserve_default=False,
        ),
    ]
