from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    client_email = models.EmailField(verbose_name='Контактный email')
    name = models.CharField(max_length=80, verbose_name='Ф.И.О. Клиента')
    comment = models.TextField(max_length=500, verbose_name='Коментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)

    def __str__(self):
        return f"{self.name}, {self.client_email}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
