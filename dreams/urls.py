from django.urls import path
from .views import DreamListView, RemoveDreamView

urlpatterns = [
        path('dream/', DreamListView.as_view()),
        path("dreams/<int:dream_id>/remove/", RemoveDreamView.as_view()),
        ]
