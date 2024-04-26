from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from mailings.forms import MailingForm
from mailings.models import Mailing, Reporting


class MailingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mailing
    login_url = 'users:login'
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'

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

    def test_func(self):
        """Проверяет разрешение доступа для пользователя.
                    :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
                    :rtype: bool
                """
        return not self.request.user.groups.filter(name='moderator').exists()


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailings_list.html'

    def get_context_data(self, **kwargs):
        """Возвращает контекст данных для использования в шаблоне представления.

            Этот метод переопределяет стандартный метод get_context_data для добавления
            дополнительных данных к контексту перед его передачей в шаблон.

            :param kwargs: Именованные аргументы.
            :return: Контекст данных для использования в шаблоне.
            :rtype: dict
            """
        context_data = super().get_context_data(**kwargs)
        mailings = context_data['object_list']
        for mailing in mailings:
            if mailing.period == 'daily':
                mailing.custom_period = 'Раз в день'
            elif mailing.period == 'weekly':
                mailing.custom_period = 'Раз в неделю'
            elif mailing.period == 'monthly':
                mailing.custom_period = 'Раз в месяц'
        context_data['object_list'] = mailings
        return context_data

    def get_queryset(self, *args, **kwargs):
        """Возвращает набор данных для запроса в представлении.

            Этот метод переопределяет стандартный метод get_queryset для фильтрации набора данных
            в зависимости от прав доступа текущего пользователя.

            :param args: Позиционные аргументы.
            :param kwargs: Именованные аргументы.
            :return: Отфильтрованный набор данных для запроса.
            :rtype: QuerySet
            """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='moderator').exists():
            queryset = queryset
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    login_url = 'users:login'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')

    def test_func(self):
        """Проверяет разрешение доступа для пользователя.
                    :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
                    :rtype: bool
                """
        return not self.request.user.groups.filter(name='moderator').exists()

    def get_success_url(self):
        from django.urls import reverse
        return reverse('mailings:update_mailings', args=[self.kwargs.get('pk')])


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    login_url = 'users:login'
    success_url = reverse_lazy('mailings:mailings_list')

    def test_func(self):
        """Проверяет разрешение доступа для пользователя.
                    :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
                    :rtype: bool
                """
        return not self.request.user.groups.filter(name='moderator').exists()


class MailingDetailView(DetailView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailings_list')


class ReportingListView(ListView):
    model = Reporting

    def get_context_data(self, *args, **kwargs):
        """Добавляет дополнительные данные в контекст шаблона.

            Эта функция переопределяет стандартный метод get_context_data,
            чтобы добавить дополнительные данные в контекст шаблона перед его передачей в шаблон.

            :param args: Позиционные аргументы.
            :param kwargs: Именованные аргументы.
            :return: Словарь с контекстом шаблона.
            :rtype: dict
            """
        context_data = super().get_context_data(*args, **kwargs)
        for context in context_data['object_list']:
            context.status_display = 'Успешно' if context.status else 'Неуспешно'
        return context_data


def toggle_activity(request: Any, pk: Any) -> Any:
    """Создает форму для активации или деактивации рассылки."""
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.is_active = not mailing.is_active
    mailing.save()

    return redirect(reverse('mailings:mailings_list'))
