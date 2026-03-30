from django.db import models
from django.contrib.auth.models import AbstractUser
from dreams.models import Dream
# Create your models here.
class User(AbstractUser):
    dream = models.ManyToManyField(Dream, blank=True)
    first_name = models.CharField(max_length=25, null=False, blank=False)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    username = models.CharField(max_length=25, null=True, blank=True, unique=True)
    email = models.CharField(max_length=75, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    join_at = models.DateTimeField(auto_now_add = True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
