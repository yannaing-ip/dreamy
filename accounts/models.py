from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    dream = models.ManyToManyField(
            "dreams.Dream",
            blank=True
        )
    first_name = models.CharField(
            max_length=25,
            null=False,
            blank=False
        )
    last_name = models.CharField(
            max_length=25,
            null=False,
            blank=False
        )
    username = models.CharField(
            max_length=25,
            null=True,
            blank=True,
            unique=True
        )
    email = models.CharField(
            max_length=75,
            null=False,
            blank=False,
            unique=True
        )
    is_active = models.BooleanField(
            default=True
        )
    join_at = models.DateTimeField(
            auto_now_add = True
        )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
            "first_name",
            "last_name",
            "username"
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Follow(models.Model):
    follower = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name="following"
        )
    following = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name="followers"
        )
    created_at = models.DateTimeField(
            auto_now_add=True
        )

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

