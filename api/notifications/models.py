from django.db import models
from django.utils.translation import gettext_lazy as _

from api.users.models import User


class Notification(models.Model):
    class Level(models.TextChoices):
        SUCCESS = "S", _("SUCCESS")
        INFO = "I", _("INFO")
        WARNING = "W", _("WARNING")
        ERROR = "E", _("ERROR")

    body = models.TextField()
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=1, choices=Level.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(default=None, null=True, blank=True)
    sent_to = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    hyper_link = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "notifications"
        verbose_name = "notification"
        verbose_name_plural = "notifications"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Notification({self.level}): {self.id}>"
