from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from django.views.generic import ListView

"""
Кастомное разрешение, разрешающее доступ только владельцу объекта.
Проверяет, что пользователь запроса является владельцем объекта Habit.
"""


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

    """
    ViewSet для работы с привычками текущего пользователя.

    Поддерживает операции CRUD:
    - list: получить список привычек пользователя
    - create: создать новую привычку, привязанную к текущему пользователю
    - retrieve: получить конкретную привычку
    - update / partial_update: обновить привычку с валидацией
    - destroy: удалить привычку

    Также реализован дополнительный action:
    - public: получить список всех публичных привычек (без авторизации)
    """


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Habit.objects.all()

    """Возвращает привычки, принадлежащие текущему пользователю,
            отсортированные по времени выполнения"""

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by("time")

    """
    Создаёт привычку, автоматически привязывая её к текущему пользователю.
    Выполняет полную валидацию модели перед сохранением
    """

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        instance.full_clean()
        instance.save()

    """Обновляет привычку с полной валидацией модели"""

    def perform_update(self, serializer):
        instance = serializer.save()  # сохраняет, но ты сам вызовешь .save() ниже
        instance.full_clean()
        instance.save()

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def public(self, request):
        """Возвращает список всех публичных привычек.
            Доступно без авторизации
        """
        habits = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet для публичных привычек.

    Позволяет только просматривать (list, retrieve) привычки,
    которые опубликованы пользователями.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]


class HabitListView(ListView):
    """
    Класс-представление для отображения HTML-страницы
    со списком привычек текущего пользователя с пагинацией.
    Использует шаблон habits/habit_list.html.
    """
    model = Habit
    template_name = 'habits/habit_list.html'
    context_object_name = 'page_obj'
    paginate_by = 5

    def get_queryset(self):
        """
        Возвращает привычки текущего пользователя.
        """
        return Habit.objects.filter(user=self.request.user)
