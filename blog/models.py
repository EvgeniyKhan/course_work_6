from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)
    count_view = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
