from rest_framework import serializers
from .models import Feed
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
