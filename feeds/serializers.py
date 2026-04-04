from rest_framework import serializers
from .models import Feed, Like, Comment
from accounts.models import User
from django.contrib.auth import get_user_model

class FeedDetailSerializer(serializers.ModelSerializer):
    from accounts.serializers import AuthorSerializer
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
class FeedForProfileSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Feed
        fields = ["id",
                  "content",
                  "created_at",
                  "like_count",
                  "comment_count",

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
