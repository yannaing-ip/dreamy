from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Feed
from .serializers import FeedSerializer, FeedDetailSerializer

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
