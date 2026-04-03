from django.urls import path
from .views import FeedView, FeedDetailView, FeedLikeView, CommentListCreateView

urlpatterns = [
        path('feeds/', FeedView.as_view()),
        path('feeds/<int:pk>', FeedDetailView.as_view()),
        path('feeds/<int:pk>/likes/', FeedLikeView.as_view()),
        path("feeds/<int:feed_id>/comments/", CommentListCreateView.as_view(), name="feed-comments"),
        ]
