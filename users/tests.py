from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY

from users.forms import CustomUserCreationForm


CustomUser = get_user_model()


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "email": "form@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_email_required(self):
        form_data = {
            "email": "",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterViewTest(TestCase):
    def test_register_view_post(self):
        data = {
            "email": "newuser@example.com",
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())
        self.assertRedirects(response, reverse("login"))

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")


class LoginLogoutViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "test@example.com",  # даже если логин по email, форма по умолчанию ожидает поле username
                "password": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"))  # POST вместо GET
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(SESSION_KEY, self.client.session)
