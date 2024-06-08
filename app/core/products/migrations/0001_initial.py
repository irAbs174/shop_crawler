# Generated by Django 5.0.6 on 2024-06-08 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_key', models.CharField(blank=True, max_length=50, null=True, verbose_name='کلید')),
                ('product_parent', models.CharField(blank=True, max_length=50, null=True, verbose_name='سایت والد')),
                ('product_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='نام')),
                ('product_price', models.CharField(blank=True, max_length=50, null=True, verbose_name='قیمت')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='تاریخ بروزرسانی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
    ]
