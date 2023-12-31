# Generated by Django 4.2.7 on 2023-11-21 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_product_stock_count_product_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour_code', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Product Colour',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'verbose_name_plural': 'Product Size',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('colour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.colour')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.size')),
            ],
            options={
                'verbose_name_plural': 'Product Attributes',
            },
        ),
        migrations.AddField(
            model_name='colour',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product'),
        ),
    ]
