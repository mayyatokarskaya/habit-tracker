from celery import shared_task
from django.utils.timezone import now

from celery import shared_task
from .models import Habit
from django.utils.timezone import localtime
from datetime import date


@shared_task
def print_hello():
    print(f"[{now()}] 👋 Привет из Celery!")


@shared_task
def send_daily_reminders():
    today = date.today()
    habits = Habit.objects.all()
    for habit in habits:

        print(
            f"[{localtime()}] Напоминание: {habit.user.email} – {habit.action} в {habit.time} ({habit.place})"
        )
