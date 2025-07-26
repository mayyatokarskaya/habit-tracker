from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitListView

router = DefaultRouter()
router.register(r"habits", HabitViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("habits/html/", HabitListView.as_view(), name="habit_list"),
]
