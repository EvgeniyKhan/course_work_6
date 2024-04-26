from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from letters.forms import MessageForm
from letters.models import Message


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Message
    login_url = 'users:login'
    form_class = MessageForm
    success_url = reverse_lazy('letters:letters_list')

    def form_valid(self, form):
        """
            Обрабатывает действия после успешной валидации формы.

            Args:
                form: Валидная форма, которую необходимо сохранить.

            Returns:
                HttpResponse: HTTP-ответ, обычно перенаправление на страницу с подтверждением или другую страницу.

            Notes:
                - Сохраняет объект из формы в базу данных.
                - Устанавливает текущего пользователя как владельца объекта.
                - Передает управление родительскому методу для выполнения дополнительных действий.
            """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        """Проверяет разрешение доступа для пользователя.

            :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
            :rtype: bool
            """
        return not self.request.user.groups.filter(name='moderator').exists()


class MessageListView(ListView):
    model = Message

    def context_data(self, *args, **kwargs):
        """
                Получает и возвращает контекст данных для представления.

                Args:
                    *args: Позиционные аргументы, передаваемые в родительский метод.
                    **kwargs: Именованные аргументы, передаваемые в родительский метод.

                Returns:
                    Словарь контекста данных для использования в шаблоне представления.
                """
        context_data = super().get_context_data(*args, **kwargs)
        context_data['message_list'] = Message.objects.all()
        return context_data

    def get_queryset(self, *args, **kwargs):
        """
            Возвращает QuerySet объектов модели в зависимости от прав доступа пользователя.

            Args:
                *args: Позиционные аргументы, передаваемые в родительский метод.
                **kwargs: Именованные аргументы, передаваемые в родительский метод.

            Returns:
                QuerySet объектов модели, отфильтрованный в соответствии с правами доступа пользователя.
            """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            queryset = queryset
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    login_url = 'users:login'
    form_class = MessageForm
    success_url = reverse_lazy('letters:letters_list')

    def test_func(self):
        """Проверяет разрешение доступа для пользователя.

            :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
            :rtype: bool
            """
        return not self.request.user.groups.filter(name='moderator').exists()


class MessageDetailView(DetailView):
    model = Message

    def get_context_data(self, *args, **kwargs):
        """
            Получает и возвращает контекст данных для представления.

            Args:
                *args: Позиционные аргументы, передаваемые в родительский метод.
                **kwargs: Именованные аргументы, передаваемые в родительский метод.

            Returns:
                Словарь контекста данных для использования в шаблоне представления.
            """
        context_data = super().get_context_data(*args, **kwargs)
        context_data['message_list'] = Message.objects.all()
        return context_data


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    login_url = 'users:login'
    success_url = reverse_lazy('letters:letters_list')

    def test_func(self):
        """Проверяет разрешение доступа для пользователя.

            :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
            :rtype: bool
            """
        return not self.request.user.groups.filter(name='moderator').exists()
