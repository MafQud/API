import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from ..locations.models import Location
from ..users.models import User


class Case(models.Model):
    class Meta:
        db_table = "cases"
        verbose_name = "case"
        verbose_name_plural = "cases"
        ordering = ["-created_at"]

    class States(models.TextChoices):
        PENDING = "PE", _("Pending")
        ACTIVE = "AC", _("Active")
        FINISHED = "DN", _("Finished")
        ARCHIVED = "AR", _("Archived")

    class Types(models.TextChoices):
        MISSING = "M", _("Missing")
        FOUND = "F", _("Found")

    type = models.CharField(max_length=1, choices=Types.choices)
    user = models.ForeignKey(User, related_name="cases", on_delete=models.CASCADE)
    state = FSMField(
        max_length=2,
        choices=States.choices,
        default=States.PENDING,
        editable=False,
    )
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_at = models.DateTimeField(null=True, default=None, blank=True)
    is_active = models.BooleanField(default=False, editable=False)

    @property
    def photo_urls(self):
        return self.photos.values_list("url", flat=True)

    def __str__(self):
        return f"{self.state} case {self.type}"

    # Pass the case to the model then add matched cases if any.
    @transition(field=state, source=States.PENDING, target=States.ACTIVE)
    def activate(self):
        from .services import case_matching_binding, process_case

        matches = process_case(self)
        case_matching_binding(matches)
        self.is_active = True

    # If User selected one of the matches to be the correct one
    @transition(field=state, source=States.ACTIVE, target=States.FINISHED)
    def finish(self):
        self.is_active = False

    # Switch to ARCHIVED state from any state except ARCHIVED
    @transition(field=state, source="+", target=States.ARCHIVED)
    def archive(self):
        self.is_active = False

    # If user selected incorrect match or lost again
    @transition(
        field=state, source=[States.FINISHED, States.ARCHIVED], target=States.ACTIVE
    )
    def activate_again(self):
        self.is_active = True

    def publish(self):
        self.posted_at = datetime.now()


class CaseDetails(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        UNKNOWN = "U", _("Unknown")

    case = models.OneToOneField(Case, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    age = models.SmallIntegerField(null=True, default=None, blank=True)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(null=True, default=None, blank=True)
    description = models.TextField(blank=True, null=True)


class CaseMatch(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="matches")
    match = models.ForeignKey(Case, on_delete=models.CASCADE)
    score = models.SmallIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )


class CasePhoto(models.Model):
    url = models.URLField()
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="photos")
