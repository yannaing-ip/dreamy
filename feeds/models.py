from django.db import models
from accounts.models import User

# Create your models here.
visibility_choice = {
        "PR" : "private",
        "PL" : "public"
    }
class Feed(models.Model):
    author = models.ForeignKey(
        User,
        models.CASCADE,
        null=False,
        blank=False
    )
    content = models.TextField(null=True, blank=True)
    visibility = models.CharField(null=False, blank=False, choices=visibility_choice)
    reactions = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "feed")

    def __str__(self):
        return f"{self.user.username} liked Feed {self.feed.id}"
