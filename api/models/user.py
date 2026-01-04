from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    avatar = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.email or self.username