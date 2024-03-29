# Generated by Django 4.1.7 on 2023-04-07 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'subscriptions',
                'verbose_name_plural': 'subscription',
            },
        ),
    ]
