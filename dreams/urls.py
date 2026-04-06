from django.urls import path
from .views import DreamListView, RemoveDreamView, DreamCreateView

urlpatterns = [
        path('dreams/', DreamListView.as_view()),
        path('dreams/create/', DreamCreateView.as_view()),
        path("dreams/<int:dream_id>/remove/", RemoveDreamView.as_view()),
        ]
