from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .models import User, Follow
from .serializers import RegisterSerializer, LoginSerializer, MeSerializer, UserFollowSerializer, ProfileSerializer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.db.models import Q
from core.paginations import SearchPagePagination

class MeView(RetrieveAPIView):
    """
    GET: Returns the authenticated user's profile including their subscribed dreams.
    """
    
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class RegisterView(CreateAPIView):
    """
    POST: Register a new user account.
    Requires email, username, first_name, last_name, and password.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

class LoginView(GenericAPIView):
    """
    POST: Authenticate with email and password.
    Returns JWT access and refresh tokens.
    """

    serializer_class = LoginSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh_token = RefreshToken.for_user(user)

        return Response({
            "access":f"{refresh_token.access_token}",
            "refresh":f"{refresh_token}"
            })

class FollowToggleView(generics.GenericAPIView):
    """
    POST: Follow or unfollow a user by their ID.
    If already following, unfollows. If not, follows.
    Cannot follow yourself.
    """
    
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if request.user == target_user:
            return Response({"error": "Cannot follow yourself"}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            follow.delete()
            return Response({"message": "Unfollowed successfully"})

        return Response({"message": "Followed successfully"})

class FollowersListView(generics.ListAPIView):
    """
    GET: Returns a list of users who follow the specified user.
    """

    serializer_class = UserFollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return User.objects.filter(following__following__id=user_id)

class FollowingListView(generics.ListAPIView):
    """
    GET: Returns a list of users that the specified user is following.
    """

    serializer_class = UserFollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return User.objects.filter(followers__follower__id=user_id)

class ProfileView(RetrieveAPIView):
    """
    GET: Returns a user's public profile including their feeds.
    Feed visibility rules are applied based on the authenticated viewer.
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["viewer"] = self.request.user
        return context

class CustomTokenRefreshView(TokenRefreshView):
    """
    POST: Refresh an expired access token using a valid refresh token.
    Returns a new access token and the same refresh token.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "access": serializer.validated_data["access"],
            "refresh": request.data.get("refresh")  # keep the same refresh token
        }, status=status.HTTP_200_OK)

class UserSearchView(generics.ListAPIView):
    """
    GET: Search users by username, first name, or last name.
    Use query param: ?q=<search_term>
    Returns up to 20 results per page. Excludes the authenticated user.
    """
    serializer_class = UserFollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SearchPagePagination

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()

        if not query:
            return User.objects.none()

        words = query.split()
        q_obj = Q()

        for word in words:
            q_obj |= Q(username__icontains=word) | Q(first_name__icontains=word) | Q(last_name__icontains=word)

        return User.objects.filter(q_obj).exclude(id=self.request.user.id).distinct().order_by("username")
