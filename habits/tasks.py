from celery import shared_task
from django.utils.timezone import localtime
from datetime import date
from .models import Habit
from utils.telegram import send_telegram_message  # <--- обязательно

@shared_task
def print_hello():
    print(f"[{localtime()}] 👋 Привет из Celery!")

@shared_task
def send_daily_reminders():
    today = date.today()
    habits = Habit.objects.all()
    for habit in habits:
        print(
            f"[{localtime()}] Напоминание: {habit.user.email} – {habit.action} в {habit.time} ({habit.place})"
        )

@shared_task
def remind_habit(habit_id):
    habit = Habit.objects.get(id=habit_id)
    message = f"⏰ Напоминание: пора выполнить привычку <b>{habit.action}</b> в {habit.time} на {habit.place}"
    send_telegram_message(message)
