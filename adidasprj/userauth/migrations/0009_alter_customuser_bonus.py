# Generated by Django 4.2.7 on 2023-12-09 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0008_customuser_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bonus',
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
    ]
