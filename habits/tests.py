import django
import os
from datetime import time
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from habits.models import Habit

# Настройка Django окружения
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


User = get_user_model()


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            action="Test Action",
            place="Test Place",
            time=time(12, 0),  # 12:00:00
            duration=60,  # 60 секунд
            frequency=1,  # ежедневно
            is_public=True,
        )

    def test_list_habits(self):
        url = reverse("habit-list")  # исправлено на "habit-list"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Test Action")

    def test_create_habit(self):
        url = reverse("habit-list")
        data = {
            # user передавать не надо, он указывается на бэкенде (self.user)
            "action": "New Action",
            "place": "New Place",
            "time": "08:00:00",
            "duration": 90,
            "frequency": 2,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(Habit.objects.last().action, "New Action")

    def test_retrieve_habit(self):
        url = reverse("habit-detail", kwargs={"pk": self.habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Test Action")

    def test_update_habit(self):
        url = reverse("habit-detail", kwargs={"pk": self.habit.pk})
        data = {"action": "Updated Action"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Updated Action")

    def test_delete_habit(self):
        url = reverse("habit-detail", kwargs={"pk": self.habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
