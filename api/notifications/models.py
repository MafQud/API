from django.db import models
from django.utils.translation import gettext_lazy as _

from api.cases.models import Case
from api.users.models import User


class Notification(models.Model):
    class Level(models.TextChoices):
        SUCCESS = "S", _("SUCCESS")
        INFO = "I", _("INFO")
        WARNING = "W", _("WARNING")
        ERROR = "E", _("ERROR")

    class Action(models.TextChoices):
        MATCHES = "M", _("Matches")
        PUBLISH = "P", _("Publish")
        DETAILS = "D", _("Details")
        NONE = "N", _("None")

    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="notifications"
    )
    level = models.CharField(max_length=1, choices=Level.choices)
    action = models.CharField(max_length=1, choices=Action.choices)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(default=None, null=True, blank=True)
    sent_to = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    class Meta:
        db_table = "notifications"
        verbose_name = "notification"
        verbose_name_plural = "notifications"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Notification({self.level}): {self.id}>"
