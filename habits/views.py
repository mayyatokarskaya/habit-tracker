from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request):
        habits = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)