# Generated by Django 4.2.7 on 2023-12-03 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0030_coupon_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='refund_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='refund_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='return_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='return_requested',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('transactions', models.TextField(default='[]')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Wallet',
            },
        ),
    ]
