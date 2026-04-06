from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Dream
from .serializers import DreamSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers as drf_serializers
# Create your views here.
class DreamListView(generics.ListAPIView):
    """
    GET: Returns a list of all available dreams. Supports ?search=<name> query param.
    POST: Add a dream to your profile by dream_id.
    """

    serializer_class = DreamSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        search = self.request.query_params.get("search", "")
        if search:
            return Dream.objects.filter(name__icontains=search)
        return Dream.objects.all()

    @extend_schema(
        methods=['POST'],
        request=inline_serializer(
            name='AddDreamToProfile',
            fields={'dream_id': drf_serializers.IntegerField()}
        ),
        responses={200: None}
    )
    def post(self, request):
        dream_id = request.data.get("dream_id")
        if not dream_id:
            return Response({"error": "dream_id is required"}, status=400)
        try:
            dream = Dream.objects.get(id=dream_id)
        except Dream.DoesNotExist:
            return Response({"error": "Dream not found"}, status=404)
        request.user.dream.add(dream)
        return Response({"message": f"Dream '{dream.name}' added successfully"})

class DreamCreateView(APIView):
    """
    POST: Create a new dream and automatically subscribe the authenticated user to it.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        description = request.data.get("description")

        if not name:
            return Response({"error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not description:
            return Response({"error": "description is required"}, status=status.HTTP_400_BAD_REQUEST)

        if Dream.objects.filter(name__iexact=name).exists():
            return Response({"error": "Dream with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

        dream = Dream.objects.create(name=name, description=description)
        request.user.dream.add(dream)

        serializer = DreamSerializer(dream)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RemoveDreamView(APIView):
    """
    POST: Unsubscribe the authenticated user from a dream by dream_id.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, dream_id):
        try:
            dream = Dream.objects.get(id=dream_id)
        except Dream.DoesNotExist:
            return Response(
                {"error": "Dream not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        if dream not in user.dream.all():
            return Response(
                {"error": "Dream not in your list"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.dream.remove(dream)

        return Response(
            {"message": "Dream removed successfully"},
            status=status.HTTP_200_OK
        )


