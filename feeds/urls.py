from django.urls import path
from .views import FeedView, FeedDetailView, FeedLikeView, CommentListCreateView, CommentDeleteView, FeedDeleteView

urlpatterns = [
        path('feeds/', FeedView.as_view()),
        path("feeds/<int:pk>/delete/", FeedDeleteView.as_view(), name="feed-delete"),
        path('feeds/<int:pk>', FeedDetailView.as_view()),
        path('feeds/<int:pk>/likes/', FeedLikeView.as_view()),
        path("feeds/<int:feed_id>/comments/", CommentListCreateView.as_view(), name="feed-comments"),
        path("feeds/<int:feed_id>/comments/<int:comment_id>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
        ]
