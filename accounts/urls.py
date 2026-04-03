from django.urls import path
from .views import RegisterView, LoginView, MeView, FollowToggleView, FollowersListView, FollowingListView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('users/<int:user_id>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
    path('users/<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('users/<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
]
