# Generated by Django 5.0.7 on 2024-07-28 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_usproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(blank=True, max_length=50, null=True, verbose_name='شناسه کاربر')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام کاربری')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='نام خانوادگی')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
    ]