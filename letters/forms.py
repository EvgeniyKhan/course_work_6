from django.forms import ModelForm

from letters.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('letter_subject', 'letter_body')
