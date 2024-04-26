from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'



class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """
            Получает объект модели из базы данных, увеличивает счетчик просмотров на 1 и сохраняет изменения.

            Args:
                queryset: QuerySet, опциональный. QuerySet, используемый для получения объекта.

            Returns:
                Объект модели с обновленным счетчиком просмотров.

            Raises:
                Может возникнуть исключение, если объект не найден в базе данных.
            """
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        """
            Получает и возвращает контекст данных для шаблона удаления блога.

            Args:
                **kwargs: Дополнительные аргументы для передачи в родительский метод.

            Returns:
                Словарь контекста данных для использования в шаблоне удаления блога.
            """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление блога'
        return context
