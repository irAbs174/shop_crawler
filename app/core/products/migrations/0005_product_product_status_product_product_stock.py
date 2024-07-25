# Generated by Django 5.0.7 on 2024-07-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_product_url_alter_product_product_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='وضعیت محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_stock',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='موجودی محصول'),
        ),
    ]