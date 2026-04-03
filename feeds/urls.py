from django.urls import path
from .views import FeedView, FeedDetailView

urlpatterns = [
        path('feeds/', FeedView.as_view()),
        path('feeds/<int:pk>', FeedDetailView.as_view())
        ]
