# Generated by Django 4.2.7 on 2023-12-02 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='minimun_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
