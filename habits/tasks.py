from celery import shared_task
from django.utils.timezone import localtime
from datetime import date

from habits.models import Habit


@shared_task
def print_hello():

@shared_task
def send_daily_reminders():
    today = date.today()
    habits = Habit.objects.all()
    for habit in habits:
        print(
            f"[{localtime()}] Напоминание: {habit.user.email} – {habit.action} в {habit.time} ({habit.place})"
        )
