# Generated by Django 4.2.7 on 2023-11-21 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_productimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount',
            new_name='discount_price',
        ),
    ]
