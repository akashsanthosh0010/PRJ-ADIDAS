# Generated by Django 4.2.7 on 2023-12-03 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_cartorder_refund_approved_cartorder_refund_requested_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorder',
            name='refund_approved',
        ),
        migrations.RemoveField(
            model_name='cartorder',
            name='refund_requested',
        ),
        migrations.RemoveField(
            model_name='cartorder',
            name='return_approved',
        ),
        migrations.RemoveField(
            model_name='cartorder',
            name='return_requested',
        ),
        migrations.AddField(
            model_name='cartorder',
            name='status',
            field=models.CharField(choices=[('return_requested', 'Return Requested'), ('refund_requested', 'Refund Requested'), ('return_approved', 'Return Approved'), ('refund_approved', 'Refund Approved')], default=None, max_length=30),
        ),
    ]
