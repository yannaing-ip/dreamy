from django.urls import path
from .views import DreamListView

urlpatterns = [
        path('dream/', DreamListView.as_view())
        ]
