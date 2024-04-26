import random
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from blog.models import Blog
from clients.forms import ClientsForm
from clients.models import Client
from mailings.models import Mailing
from mailings.services import (get_cache_for_active_mailings,
                               get_cache_for_mailings)


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    login_url = 'users:login'
    form_class = ClientsForm
    success_url = reverse_lazy('clients:client_list')
    template_name = 'clients/clients_form.html'

    def form_valid(self, form):
        """Обрабатывает данные формы при их корректной валидации.

            Этот метод вызывается при успешной валидации данных формы. Он сохраняет объект,
            устанавливает владельца объекта в текущего пользователя и затем вызывает
            соответствующий метод родительского класса.

            :param form: Форма, содержащая валидные данные.
            :return: Результат выполнения метода form_valid родительского класса.
            """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self) -> Any:
        """Проверяет разрешение доступа для пользователя.

            :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
            :rtype: bool
            """
        return not self.request.user.groups.filter(name='moderator').exists()


class ClientListView(ListView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        """
            Получает контекст данных для представления и добавляет список клиентов в контекст.

            Args:
                *args: Позиционные аргументы, передаваемые в родительский метод.
                **kwargs: Именованные аргументы, передаваемые в родительский метод.

            Returns:
                Словарь контекста данных с добавленным списком всех клиентов.
            """
        context_data = super().get_context_data(*args, **kwargs)
        context_data['client_list'] = Client.objects.all()
        return context_data

    def get_queryset(self, **kwargs: Any) -> Any:
        """
            Возвращает QuerySet объектов модели в зависимости от прав доступа пользователя.

            Args:
                **kwargs: Дополнительные аргументы, которые могут быть переданы в родительский метод.

            Returns:
                QuerySet объектов модели, отфильтрованный в соответствии с правами доступа пользователя.

            Raises:
                Any: Может возникнуть исключение, если пользователь не имеет прав доступа.
            """
        queryset = super().get_queryset(**kwargs)
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            queryset = queryset
        else:
            queryset = queryset.filter(owner=self.request.user.id)
        return queryset


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    login_url = 'users:login'
    form_class = ClientsForm
    template_name = 'clients/clients_form.html'
    success_url = reverse_lazy('clients:client_list')

    def test_func(self) -> Any:
        """Проверяет разрешение доступа для пользователя.

            :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
            :rtype: bool
            """
        return not self.request.user.groups.filter(name='moderator').exists()


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    login_url = 'users:login'
    template_name = 'clients/clients_confirm_delete.html'
    success_url = reverse_lazy('clients:clients_list')

    def test_func(self) -> Any:
        """Проверяет разрешение доступа для пользователя.

            :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
            :rtype: bool
            """
        return not self.request.user.groups.filter(name='moderator').exists()


class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/clients_detail.html'


class HomeView(TemplateView):
    template_name = 'clients/home.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        """
            Получает и возвращает контекст данных для представления.

            Args:
                **kwargs: Дополнительные аргументы, которые могут быть переданы в родительский метод.

            Returns:
                Словарь контекста данных для использования в шаблоне представления.
            """
        context_data = super().get_context_data(**kwargs)
        context_data["mailings_count"] = get_cache_for_mailings()
        context_data["active_mailings_count"] = get_cache_for_active_mailings()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data["blog_list"] = blog_list[:3]
        context_data["clients_count"] = len(Client.objects.all())
        return context_data
