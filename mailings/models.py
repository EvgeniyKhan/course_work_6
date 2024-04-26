from django.db import models

from clients.models import Client
from letters.models import Message
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATED, 'Запущена'),
        (STATUS_STARTED, 'Создана'),
        (STATUS_DONE, 'Завершена')
    )

    name = models.CharField(max_length=100, verbose_name='Имя рассылки', **NULLABLE)
    start_time = models.DateTimeField(verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Период')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщения', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активация')

    def __str__(self):
        return f"Рассылка: {self.name}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Reporting(models.Model):
    time_log = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.BooleanField(verbose_name='Статус попытки')
    mailings = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)

    def __str__(self):
        return f'{self.time_log}, {self.status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
