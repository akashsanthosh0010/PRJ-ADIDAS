# Generated by Django 4.2.7 on 2023-12-09 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0007_customuser_referral_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bonus',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
