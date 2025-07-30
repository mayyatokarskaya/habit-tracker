from datetime import datetime, timedelta
from django.utils.timezone import now
from celery import shared_task
from .models import Habit
from utils.telegram import send_telegram_message

from dotenv import load_dotenv

load_dotenv()


@shared_task
def send_daily_reminders():
    current_time = now().time()
    time_range_start = (
        datetime.combine(datetime.today(), current_time) - timedelta(minutes=5)
    ).time()
    time_range_end = (
        datetime.combine(datetime.today(), current_time) + timedelta(minutes=5)
    ).time()

    habits = Habit.objects.filter(time__gte=time_range_start, time__lte=time_range_end)
    for habit in habits:
        remind_habit.delay(habit.id)


@shared_task
def remind_habit(habit_id):
    habit = Habit.objects.get(id=habit_id)
    message = f"⏰ Напоминание: пора выполнить привычку <b>{habit.action}</b> в {habit.time} на {habit.place}"
    send_telegram_message(message)
