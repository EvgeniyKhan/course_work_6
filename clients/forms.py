from django.forms import ModelForm

from clients.models import Client


class ClientsForm(ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'client_email', 'comment',)
