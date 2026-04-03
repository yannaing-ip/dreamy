from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Feed, Like, Comment
from rest_framework import status
from .serializers import FeedSerializer, FeedDetailSerializer, LikeSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class FeedView(generics.ListCreateAPIView):

    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_dreams = self.request.user.dream.all()
        return Feed.objects.filter(dreams__in=user_dreams).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedDetailView(generics.RetrieveAPIView):

    serializer_class = FeedDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Feed.objects.all()

class FeedLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        Toggle like: if already liked, remove; if not, add like.
        """
        try:
            feed = Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            return Response({"error": "Feed not found"}, status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(user=request.user, feed=feed).first()

        if like:
            # User already liked -> remove
            like.delete()
            return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        else:
            # User hasn’t liked yet -> add like
            Like.objects.create(user=request.user, feed=feed)
            return Response({"message": "Liked successfully"}, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        """
        Retrieve all users who liked this feed.
        """
        try:
            feed = Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            return Response({"error": "Feed not found"}, status=status.HTTP_404_NOT_FOUND)

        users = feed.likes.select_related('user').all().values('user__id', 'user__first_name', 'user__last_name')
        # Transform to list of dicts
        response = [{"id": u["user__id"], "first_name": u["user__first_name"], "last_name": u["user__last_name"]} for u in users]
        return Response(response)

class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, feed_id):
        try:
            feed = Feed.objects.get(id=feed_id)
        except Feed.DoesNotExist:
            return Response({"error": "Feed not found"}, status=status.HTTP_404_NOT_FOUND)

        comments = feed.comments.select_related("author").all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, feed_id):
        try:
            feed = Feed.objects.get(id=feed_id)
        except Feed.DoesNotExist:
            return Response({"error": "Feed not found"}, status=status.HTTP_404_NOT_FOUND)

        content = request.data.get("content")
        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(author=request.user, feed=feed, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
