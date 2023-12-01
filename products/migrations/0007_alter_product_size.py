# Generated by Django 4.2.7 on 2023-11-29 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, choices=[('S', 'Small (18cm - 6 portions)'), ('M', 'Medium (26cm - 12 portions)'), ('L', 'Large (36cm - 25 portions)')], max_length=5, null=True),
        ),
    ]
