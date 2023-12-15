# Generated by Django 4.2.7 on 2023-11-18 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_topcategory_options_remove_topcategory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='top_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.topcategory'),
        ),
    ]