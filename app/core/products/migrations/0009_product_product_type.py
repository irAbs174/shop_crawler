# Generated by Django 5.0.6 on 2024-07-31 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_botusers_created_at_botusers_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='محصول مرجع'),
        ),
    ]
