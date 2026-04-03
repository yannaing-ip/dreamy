from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Dream
from .serializers import DreamSerializer
from rest_framework import generics
# Create your views here.
class DreamListView(generics.ListAPIView):
    serializer_class = DreamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
       search = self.request.query_params.get("search", "")
       if search:
           return Dream.objects.filter(name__icontains=search)
       return Dream.objects.all()

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






