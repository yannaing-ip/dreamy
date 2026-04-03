from rest_framework import serializers
from .models import Feed, Like, User
from django.contrib.auth import get_user_model
from accounts.serializers import MeSerializer, AuthorSerializer

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = [
                "id",
                "content",
                "dreams",
                ]

class FeedDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Feed
        fields = [
                "author",
                "id",
                "content",
                "like_count",
                "comment_count",
                "visibility",
                "created_at",
                "updated_at"
                ]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
