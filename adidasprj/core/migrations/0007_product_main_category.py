# Generated by Django 4.2.7 on 2023-11-16 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_category_main_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.maincategory'),
        ),
    ]