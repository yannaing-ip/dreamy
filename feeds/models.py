from django.db import models
from accounts.models import Account
# Create your models here.
visibility_choice = {
        "PR" : "private",
        "PL" : "public"
    }
class Feed(models.Model):
    owner = models.ForeignKey(Account, models.CASCADE, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    visibility = models.CharField(null=False, blank=False, choices=visibility_choice)
    reactions = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
