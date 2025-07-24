from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'is_pleasant', 'is_public', 'frequency', 'time')
    list_filter = ('is_pleasant', 'is_public', 'frequency')
    search_fields = ('action', 'place', 'reward')
