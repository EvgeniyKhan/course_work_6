from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        email = 'Khan@admin.ru'
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(
                email=email,
                first_name='Admin',
                last_name='Sky_Store',
                is_staff=True,
                is_superuser=True
            )

            user.set_password('Admin')
            user.save()
        else:
            print(f'Пользователь с email "{email}" уже существует.')
