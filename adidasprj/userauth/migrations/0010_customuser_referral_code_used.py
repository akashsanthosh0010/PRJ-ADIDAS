# Generated by Django 4.2.7 on 2023-12-09 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0009_alter_customuser_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referral_code_used',
            field=models.BooleanField(default=False),
        ),
    ]
