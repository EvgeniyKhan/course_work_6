# Generated by Django 5.0.4 on 2024-04-22 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0003_reporting'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активация'),
        ),
    ]
