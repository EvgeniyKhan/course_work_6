from django import forms
from django.contrib.auth.forms import (PasswordResetForm, UserChangeForm,
                                       UserCreationForm)

from mailings.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserPasswordRecoveryForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

