from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .validators import is_phone


class User(AbstractUser):
    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    first_name = None  # type: ignore
    last_name = None  # type: ignore

    full_name = models.CharField(max_length=256)
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=10, unique=True, validators=[is_phone])

    id_exp_date = models.DateTimeField(null=True, blank=True)
    id_photo_url = models.ImageField(upload_to="id-photos/")

    firebase_token = models.CharField(max_length=256, unique=True, blank=True)

    def renew_id(self, days: int = 365) -> None:
        self.id_exp_date = timezone.now() + timezone.timedelta(days=days)

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self) -> str:
        return self.username
