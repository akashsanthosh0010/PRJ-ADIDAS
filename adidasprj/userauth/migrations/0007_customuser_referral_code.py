# Generated by Django 4.2.7 on 2023-12-09 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0006_customuser_password_reset_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referral_code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
