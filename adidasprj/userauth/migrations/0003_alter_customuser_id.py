# Generated by Django 4.2.7 on 2023-11-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_alter_customuser_email_alter_customuser_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
