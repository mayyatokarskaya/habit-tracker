from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    frequency = models.PositiveSmallIntegerField(default=1)  # в днях
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveSmallIntegerField()  # в секундах
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Укажите либо награду, либо связанную привычку, но не оба.")
        if self.duration > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("В связанные привычки можно указывать только приятные привычки.")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь награду или связанную привычку.")
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем раз в 7 дней.")

    def __str__(self):
        return self.action

