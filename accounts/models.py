from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Account(AbstractUser):
    first_name = models.CharField(max_length=25, null=False, blank=False)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    email = models.CharField(max_length=75, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    join_at = models.DateTimeField(auto_now_add = True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{first_name} {last_name}"
