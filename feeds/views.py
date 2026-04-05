from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Feed, Like, Comment
from rest_framework import status
from .serializers import FeedDetailSerializer, LikeSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from feeds.services import get_visible_feeds

class FeedView(generics.ListCreateAPIView):
    """
    GET: Returns feeds visible to the authenticated user based on visibility rules.
    POST: Create a new feed post. Requires content, visibility, and dreams.
    """

    serializer_class = FeedDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        # Step 1: apply visibility rules
        queryset = get_visible_feeds(user)

        # Step 2: filter by user dreams
        user_dreams = user.dream.all()

        queryset = queryset.filter(
            dreams__in=user_dreams
        ).distinct()

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedDeleteView(generics.DestroyAPIView):
    """
    DELETE: Delete a feed post. Only the author can delete their own feed.
    """

    queryset = Feed.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        feed = self.get_object()
        if request.user != feed.author:
            return Response({"error": "Not allowed"}, status=403)
        feed.delete()
        return Response({"message": "Feed deleted successfully"}, status=status.HTTP_200_OK)

class FeedDetailView(generics.RetrieveAPIView):
    """
    GET: Returns the details of a specific feed post.
    """

    serializer_class = FeedDetailSerializer
    permission_classes = [IsAuthenticated]
    queryset = Feed.objects.all()

class FeedLikeView(APIView):
    """
    GET: Returns a list of users who liked this feed.
    POST: Toggle like on a feed. Adds like if not liked, removes if already liked.
    """

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
    """
    GET: Returns all comments on a specific feed.
    POST: Add a comment to a feed. Requires content field.
    """

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

class CommentDeleteView(APIView):
    """
    DELETE: Delete a comment. Only the comment author or feed author can delete.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, feed_id, comment_id):
        try:
            feed = Feed.objects.get(id=feed_id)
        except Feed.DoesNotExist:
            return Response({"error": "Feed not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = Comment.objects.get(id=comment_id, feed=feed)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Only comment author or feed author can delete
        if request.user != comment.author and request.user != feed.author:
            return Response({"error": "You don't have permission to delete this comment"},
                            status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)
