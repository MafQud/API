from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

from api.common.validators import is_phone
from api.locations.models import Location


class User(AbstractUser):
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    name = models.CharField(max_length=256)
    username = models.CharField(max_length=10, unique=True, validators=[is_phone])

    id_exp_date = models.DateTimeField(null=True, blank=True)

    firebase_token = models.CharField(max_length=256, unique=True, blank=True)

    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, null=True, related_name="user"
    )

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def is_verified(self) -> bool:
        return self.id_exp_date and self.id_exp_date > timezone.now()

    def get_absolute_url(self) -> str:
        return reverse("apis:users:get_user", args=[str(self.id)])

    def renew_id(self, days: int = 365) -> None:
        self.id_exp_date = timezone.now() + timezone.timedelta(days=days)

    def __str__(self) -> str:
        return self.username
