from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from dreams.models import Dream
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status  # add status here
from rest_framework.views import APIView
from .models import Dream
from .serializers import DreamSerializer

class DreamListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )
        self.dream1 = Dream.objects.create(
            name = "Flying",
            description = "Dreams about flying"
        )
        self.dream2 = Dream.objects.create(
            name = "Falling",
            description = "Dreams about falling"
        )
        self.client.force_authenticate(user = self.user)

    def test_list_dreams(self):
        response = self.client.get('/api/dream/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_dreams_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.get('/api/dream/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_dream_by_name(self):
        response = self.client.get('/api/dream/?search=fly')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Flying")

    def test_search_dream_no_results(self):
        response = self.client.get('/api/dream/?search=xyz')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class DreamSubscribeTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )
        self.dream = Dream.objects.create(
            name = "Flying",
            description = "Dreams about flying"
        )
        self.client.force_authenticate(user = self.user)

    def test_subscribe_to_dream(self):
        response = self.client.post('/api/dream/', {
            "dream_id": self.dream.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.dream, self.user.dream.all())

    def test_subscribe_invalid_dream_id(self):
        response = self.client.post('/api/dream/', {
            "dream_id": 9999
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_missing_dream_id(self):
        response = self.client.post('/api/dream/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscribe_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.post('/api/dream/', {
            "dream_id": self.dream.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DreamUnsubscribeTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )
        self.dream = Dream.objects.create(
            name = "Flying",
            description = "Dreams about flying"
        )
        self.user.dream.add(self.dream)
        self.client.force_authenticate(user = self.user)

    def test_unsubscribe_from_dream(self):
        response = self.client.post(f'/api/dreams/{self.dream.id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.dream, self.user.dream.all())

    def test_unsubscribe_dream_not_in_list(self):
        other_dream = Dream.objects.create(
            name = "Falling",
            description = "Dreams about falling"
        )
        response = self.client.post(f'/api/dreams/{other_dream.id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsubscribe_invalid_dream_id(self):
        response = self.client.post('/api/dreams/9999/remove/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsubscribe_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.post(f'/api/dreams/{self.dream.id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



