from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, Follow
from feeds.models import Feed, Like, Comment
from dreams.models import Dream


class FeedCRUDTest(TestCase):

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

    def test_create_feed(self):
        response = self.client.post('/api/feeds/', {
            "content": "I dreamed I was flying",
            "visibility": "PL",
            "dreams": [self.dream.id]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feed.objects.count(), 1)

    def test_create_feed_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.post('/api/feeds/', {
            "content": "I dreamed I was flying",
            "visibility": "PL",
            "dreams": [self.dream.id]
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_feed_list(self):
        Feed.objects.create(
            author = self.user,
            content = "Test feed",
            visibility = "PL"
        )
        response = self.client.get('/api/feeds/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_feed_detail(self):
        feed = Feed.objects.create(
            author = self.user,
            content = "Test feed",
            visibility = "PL"
        )
        response = self.client.get(f'/api/feeds/{feed.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Test feed")

    def test_delete_feed_by_author(self):
        feed = Feed.objects.create(
            author = self.user,
            content = "Test feed",
            visibility = "PL"
        )
        response = self.client.delete(f'/api/feeds/{feed.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Feed.objects.count(), 0)

    def test_delete_feed_by_non_author(self):
        other = User.objects.create_user(
            email = "other@example.com",
            username = "otheruser",
            first_name = "Other",
            last_name = "User",
            password = "testpass123"
        )
        feed = Feed.objects.create(
            author = other,
            content = "Other's feed",
            visibility = "PL"
        )
        response = self.client.delete(f'/api/feeds/{feed.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Feed.objects.count(), 1)


class FeedVisibilityTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = User.objects.create_user(
            email = "author@example.com",
            username = "author",
            first_name = "Author",
            last_name = "User",
            password = "testpass123"
        )
        self.follower = User.objects.create_user(
            email = "follower@example.com",
            username = "follower",
            first_name = "Follower",
            last_name = "User",
            password = "testpass123"
        )
        self.stranger = User.objects.create_user(
            email = "stranger@example.com",
            username = "stranger",
            first_name = "Stranger",
            last_name = "User",
            password = "testpass123"
        )
        Follow.objects.create(follower = self.follower, following = self.author)

    def test_public_feed_visible_to_stranger(self):
        Feed.objects.create(
            author = self.author,
            content = "Public feed",
            visibility = "PL"
        )
        self.client.force_authenticate(user = self.stranger)
        response = self.client.get('/api/feeds/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_private_feed_visible_to_follower(self):
        feed = Feed.objects.create(
            author = self.author,
            content = "Private feed",
            visibility = "PR"
        )
        self.client.force_authenticate(user = self.follower)
        from feeds.services import get_visible_feeds
        qs = get_visible_feeds(self.follower)
        self.assertIn(feed, qs)

    def test_private_feed_hidden_from_stranger(self):
        feed = Feed.objects.create(
            author = self.author,
            content = "Private feed",
            visibility = "PR"
        )
        from feeds.services import get_visible_feeds
        qs = get_visible_feeds(self.stranger)
        self.assertNotIn(feed, qs)


class LikeTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )
        self.feed = Feed.objects.create(
            author = self.user,
            content = "Test feed",
            visibility = "PL"
        )
        self.client.force_authenticate(user = self.user)

    def test_like_feed(self):
        response = self.client.post(f'/api/feeds/{self.feed.id}/likes/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(
            user = self.user,
            feed = self.feed
        ).exists())

    def test_unlike_feed(self):
        Like.objects.create(user = self.user, feed = self.feed)
        response = self.client.post(f'/api/feeds/{self.feed.id}/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(
            user = self.user,
            feed = self.feed
        ).exists())

    def test_like_count_increases(self):
        self.client.post(f'/api/feeds/{self.feed.id}/likes/')
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.like_count, 1)

    def test_like_count_decreases(self):
        Like.objects.create(user = self.user, feed = self.feed)
        self.feed.like_count = 1
        self.feed.save()
        self.client.post(f'/api/feeds/{self.feed.id}/likes/')
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.like_count, 0)

    def test_get_likes_list(self):
        Like.objects.create(user = self.user, feed = self.feed)
        response = self.client.get(f'/api/feeds/{self.feed.id}/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_like_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.post(f'/api/feeds/{self.feed.id}/likes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email = "yan@example.com",
            username = "yannaing",
            first_name = "Yan",
            last_name = "Naing",
            password = "testpass123"
        )
        self.feed = Feed.objects.create(
            author = self.user,
            content = "Test feed",
            visibility = "PL"
        )
        self.client.force_authenticate(user = self.user)

    def test_add_comment(self):
        response = self.client.post(f'/api/feeds/{self.feed.id}/comments/', {
            "content": "Nice dream!"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_add_comment_missing_content(self):
        response = self.client.post(f'/api/feeds/{self.feed.id}/comments/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_count_increases(self):
        self.client.post(f'/api/feeds/{self.feed.id}/comments/', {
            "content": "Nice dream!"
        })
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.comment_count, 1)
    def test_get_comments(self):
        Comment.objects.create(
                author = self.user,
                feed = self.feed,
                content = "Nice dream!"
                )
        response = self.client.get(f'/api/feeds/{self.feed.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_delete_comment_by_author(self):
        comment = Comment.objects.create(
            author = self.user,
            feed = self.feed,
            content = "Nice dream!"
        )
        response = self.client.delete(
            f'/api/feeds/{self.feed.id}/comments/{comment.id}/delete/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_comment_by_stranger(self):
        stranger = User.objects.create_user(
            email = "stranger@example.com",
            username = "stranger",
            first_name = "Stranger",
            last_name = "User",
            password = "testpass123"
        )
        comment = Comment.objects.create(
            author = self.user,
            feed = self.feed,
            content = "Nice dream!"
        )
        self.client.force_authenticate(user = stranger)
        response = self.client.delete(
            f'/api/feeds/{self.feed.id}/comments/{comment.id}/delete/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_unauthenticated(self):
        self.client.force_authenticate(user = None)
        response = self.client.post(f'/api/feeds/{self.feed.id}/comments/', {
            "content": "Nice dream!"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
