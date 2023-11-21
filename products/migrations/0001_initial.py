# Generated by Django 4.2.7 on 2023-11-20 23:12

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Format: required, max_length=100', max_length=100, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(help_text='Format: required, max_length=150', max_length=150, unique=True, verbose_name='Category Slug')),
                ('is_active', models.BooleanField(default=False)),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
    ]