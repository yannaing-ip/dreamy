from django.db import models
from accounts.models import User
from dreams.models import Dream

# Create your models here.
visibility_choice = {
        "PR" : "private",
        "PL" : "public",
        "PT" : "protected"
    }

class Feed(models.Model):
    author = models.ForeignKey(
        User,
        models.CASCADE,
        null=False,
        blank=False
        )
    content = models.TextField(
            null=False,
            blank=False
        )
    dreams = models.ManyToManyField(
        Dream,
        related_name="feeds"
    )
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    visibility = models.CharField(
            null=False,
            blank=False,
            choices=visibility_choice
        )
    created_at = models.DateTimeField(
            auto_now_add=True
        )
    updated_at = models.DateTimeField(
            auto_now=True
        )

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(
            auto_now_add=True
        )

    class Meta:
        unique_together = ("user", "feed")

    def __str__(self):
        return f"{self.user.username} liked Feed {self.feed.id}"


class Comment(models.Model):
    author = models.ForeignKey(
            User,
            on_delete=models.CASCADE
        )
    feed = models.ForeignKey(
            Feed,
            on_delete=models.CASCADE,
            related_name="comments"
        )
    content = models.TextField()
    created_at = models.DateTimeField(
            auto_now_add=True
        )

    def __str__(self):
        return f"{self.author.username} on Feed {self.feed.id}"


