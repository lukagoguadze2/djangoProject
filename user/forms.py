from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.forms import TextInput, CharField, PasswordInput, EmailField

from user.models import User


class AuthForm(AuthenticationForm):
    username = UsernameField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username or email',
            }
        )
    )

    password = CharField(
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                'placeholder': 'Enter your password',
                "autocomplete": "current-password"
            }
        ),
    )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = UsernameField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
            }
        )
    )

    email = EmailField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }
        )
    )

    password1 = CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password',
            }
        )
    )

    password2 = CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm your password',
            }
        )
    )
