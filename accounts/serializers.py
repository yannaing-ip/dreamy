from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from dreams.serializers import DreamSerializer

User = get_user_model()

class MeSerializer(serializers.ModelSerializer):
    dream = DreamSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "dream"
                ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
                "email",
                "username",
                "first_name",
                "last_name",
                "password"
                ]
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user

class LoginSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data
