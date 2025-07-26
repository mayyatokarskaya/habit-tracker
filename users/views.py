from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.

    Использует форму CustomUserCreationForm для создания пользователя с email.
    После успешной регистрации выполняет автоматический вход пользователя
    и перенаправляет на страницу логина.
    """
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """
        Обработка успешного заполнения формы регистрации.

        Сохраняет пользователя, выполняет вход и перенаправляет на логин.
        """
        user = form.save()
        login(self.request, user)
        return redirect("login")


class CustomLoginView(LoginView):
    """
    Представление для авторизации пользователя.

    Использует шаблон users/login.html.
    """
    template_name = "users/login.html"


class CustomLogoutView(LogoutView):
    """
    Представление для выхода пользователя из системы.

    После выхода перенаправляет на страницу логина.
    """
    next_page = reverse_lazy("login")
