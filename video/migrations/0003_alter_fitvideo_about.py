# Generated by Django 4.1.7 on 2023-03-17 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_fitvideo_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitvideo',
            name='about',
            field=models.TextField(blank=True, verbose_name='about'),
        ),
    ]