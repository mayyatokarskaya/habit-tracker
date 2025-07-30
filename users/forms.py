from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = forms.EmailInput(attrs={"placeholder": "Email"})
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"placeholder": "Пароль"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Повторите пароль"}
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"autofocus": True})
    )

    def confirm_login_allowed(self, user):
        pass
