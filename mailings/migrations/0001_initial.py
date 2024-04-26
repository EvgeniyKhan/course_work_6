# Generated by Django 5.0.4 on 2024-04-21 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя рассылки')),
                ('start_time', models.DateTimeField(verbose_name='Время начала рассылки')),
                ('end_time', models.DateTimeField(verbose_name='Время окончания рассылки')),
                ('period', models.CharField(choices=[('daily', 'Ежедневная'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], default='daily', max_length=20, verbose_name='Период')),
                ('status', models.CharField(choices=[('created', 'Запущена'), ('started', 'Создана'), ('done', 'Завершена')], default='created', max_length=20, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
    ]