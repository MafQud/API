from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from api.files.models import File

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
    thumbnail = models.OneToOneField(File, on_delete=models.CASCADE)

    @property
    def photo_urls(self):
        return [photo.file.url for photo in self.photos.all()]

    def __str__(self):
        return f"{self.state} case {self.type}"

    # Pass the case to the model then add matched cases if any.
    @transition(field=state, source=States.PENDING, target=States.ACTIVE)
    def activate(self):
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
        self.posted_at = timezone.now()


class CaseDetails(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        UNKNOWN = "U", _("Unknown")

    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name="details")
    name = models.CharField(max_length=128, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    age = models.SmallIntegerField(null=True, blank=True)
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, null=True, blank=True
    )
    last_seen = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class CaseMatch(models.Model):
    missing = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="missing_matches"
    )
    found = models.ForeignKey(
        Case, on_delete=models.CASCADE, related_name="found_matches"
    )
    score = models.SmallIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )


class CasePhoto(models.Model):
    file = models.OneToOneField(File, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="photos")


class CaseContacts(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="contacts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    contacted_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True, default=None)
