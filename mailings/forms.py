from django import forms
from django.forms import BooleanField, DateTimeInput, ModelForm

from mailings.models import Mailing


class StyleFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'from-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ('is_active', 'owner')
        widgets = {
            'start_datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': DateTimeInput(attrs={'type': 'datetime-local'})
        }
