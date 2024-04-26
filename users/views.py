import random
import string
from typing import Any
from urllib import request

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, ListView, UpdateView

from config import settings
from users.forms import (UserPasswordRecoveryForm, UserProfileForm,
                         UserRegisterForm)
from users.models import User


def generate_random_password():
    length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def activate_user(request):
    key = request.GET.get('key')
    current_user = User.objects.filter(is_active=False)
    for user in current_user:
        if str(user.token) == str(key):
            user.is_active = True
            user.token = None
            user.save()
    response = redirect(reverse_lazy('users:login'))
    return response


def toggle_activity(request: Any, pk: Any) -> Any:
    """ Функция для переключения активности пользователя """
    user_activity = get_object_or_404(User, pk=pk)
    user_activity.is_active = not user_activity.is_active  # Инвертируем значение is_active
    user_activity.save()

    return redirect(reverse('users:manager_list'))


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form: Any) -> Any:
        new_user = form.save()
        new_user.is_active = False
        secret_token = ''.join([str(random.randint(0, 9)) for string in range(10)])
        new_user.token = secret_token
        message = (f'Для подтверждения вашего Е-mail перейдите по ссылке'
                   f' http://127.0.0.1:8001/users/verify/?token={secret_token}')
        send_mail(
            subject='Подтверждение регистрации',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserPasswordRecoveryView(FormView):
    template_name = 'users/password_recovery.html'
    form_class = UserPasswordRecoveryForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data.get['email']
        try:
            user = User.objects.filter(email=email).first()
        except User.DonesNotExist:
            return render(request, 'password_recovery.html',
                          {'error': 'Пользователь с таким email не найден'})
        new_password = generate_random_password()
        user.password = make_password(new_password)
        user.save()
        subject = 'Восстановление пароля'
        message = f'Ваш новый пароль {new_password}'
        from_email = settings.EMAIL_HOST_USER
        recipients = [user.email]
        send_mail(subject, message, from_email, recipients, fail_silently=False)
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ManagerListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/manager.html'

    def test_func(self):
        """Проверяет разрешение доступа для пользователя.
            :return: True, если пользователь имеет разрешение на доступ, и False в противном случае.
            :rtype: bool
        """
        return self.request.user.is_superuser or self.request.user.groups.filter(name='moderator').exists()
