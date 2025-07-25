from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        # дублируем логику из модели
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant")
        duration = data.get("duration")
        frequency = data.get("frequency")

        if reward and related_habit:
            raise serializers.ValidationError(
                "Укажите либо награду, либо связанную привычку, но не оба."
            )
        if duration > 120:
            raise serializers.ValidationError(
                "Время выполнения не может превышать 120 секунд."
            )
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки можно указывать только приятные привычки."
            )
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь награду или связанную привычку."
            )
        if frequency < 1 or frequency > 7:
            raise serializers.ValidationError(
                "Частота привычки должна быть от 1 до 7 дней."
            )
        return data
