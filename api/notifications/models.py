from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    class Level(models.TextChoices):
        SUCCESS = "S", _("SUCCESS")
        INFO = "I", _("INFO")
        WARNING = "W", _("WARNING")
        ERROR = "E", _("ERROR")

    level = models.CharField(max_length=1, choices=Level.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(default=None, null=True, blank=True)
    # TODO : sent_to field
    # TODO : hyper_link field

    class Meta:
        db_table = "notifications"
        verbose_name = "notification"
        verbose_name_plural = "notifications"

    def __str__(self) -> str:
        return f"<Notification({self.level}): {self.id}"
