from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Follow


class UserRegistrationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'

    def test_register_success(self):
        data = {
            "email": "yan@example.com",
            "username": "yannaing",
            "first_name": "Yan",
            "last_name": "Naing",
            "password": "testpass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_missing_fields(self):
        data = {"email": "yan@example.com"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        data = {
            "email": "yan@example.com",
            "username": "yannaing",
            "first_name": "Yan",
            "last_name": "Naing",
            "password": "testpass123"
        }
        self.client.post(self.register_url, data)
        data["username"] = "yannaing2"
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        data = {
            "email": "yan@example.com",
            "username": "yannaing",
            "first_name": "Yan",
            "last_name": "Naing",
            "password": "testpass123"
        }
        self.client.post(self.register_url, data)
        data["email"] = "yan2@example.com"
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/login/'
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            "email": "yan@example.com",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.login_url, {
            "email": "yan@example.com",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_email(self):
        response = self.client.post(self.login_url, {
            "email": "wrong@example.com",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MeViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.me_url = '/api/me/'
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )

    def test_me_authenticated(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "yan@example.com")

    def test_me_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FollowTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email = "user1@example.com",
            username = "user1",
            first_name = "User",
            last_name = "One",
            password = "testpass123"
        )
        self.user2 = User.objects.create_user(
            email = "user2@example.com",
            username = "user2",
            first_name = "User",
            last_name = "Two",
            password = "testpass123"
        )
        self.client.force_authenticate(user = self.user1)

    def test_follow_user(self):
        response = self.client.post(f'/api/users/{self.user2.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Follow.objects.filter(
            follower = self.user1,
            following = self.user2
        ).exists())

    def test_unfollow_user(self):
        Follow.objects.create(follower = self.user1, following = self.user2)
        response = self.client.post(f'/api/users/{self.user2.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(
            follower = self.user1,
            following = self.user2
        ).exists())

    def test_follow_yourself(self):
        response = self.client.post(f'/api/users/{self.user1.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_count_increases(self):
        self.client.post(f'/api/users/{self.user2.id}/follow/')
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.following_count, 1)
        self.assertEqual(self.user2.followers_count, 1)

    def test_unfollow_count_decreases(self):
        Follow.objects.create(follower = self.user1, following = self.user2)
        self.user1.following_count = 1
        self.user1.save()
        self.user2.followers_count = 1
        self.user2.save()
        self.client.post(f'/api/users/{self.user2.id}/follow/')
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.following_count, 0)
        self.assertEqual(self.user2.followers_count, 0)

    def test_follow_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.post(f'/api/users/{self.user2.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserSearchTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )
        self.other = User.objects.create_user(
            email = "other@example.com",
            username = "otheruser",
            first_name = "Other",
            last_name = "User",
            password = "testpass123"
        )
        self.client.force_authenticate(user = self.user)

    def test_search_by_username(self):
        response = self.client.get('/api/search/?q=otheruser')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_search_excludes_self(self):
        response = self.client.get('/api/search/?q=yan')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [u["id"] for u in response.data["results"]]
        self.assertNotIn(self.user.id, ids)

    def test_search_empty_query(self):
        response = self.client.get('/api/search/?q=')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_search_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.get('/api/search/?q=other')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
