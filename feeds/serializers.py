from rest_framework import serializers
from .models import Feed, Like, Comment
from accounts.models import User
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

class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source="author.first_name", read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author_first_name",
            "author_last_name",
            "content",
            "created_at",
        ]
