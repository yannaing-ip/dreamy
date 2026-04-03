from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(CreateAPIView):

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
