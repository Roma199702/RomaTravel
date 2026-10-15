
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RomaTravelLoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=30,
        error_messages={
            'max_length': 'El usuario no puede superar los 30 caracteres.'
        }
    )

    password = forms.CharField(
        max_length=30,
        strip=False,
        widget=forms.PasswordInput,
        error_messages={
            'max_length': 'La contraseña no puede superar los 30 caracteres.'
        }
    )
