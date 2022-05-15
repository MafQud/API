from django.conf import settings
from django.db import models
from django.utils import timezone

from api.files.enums import FileUploadStorage
from api.files.utils import file_generate_upload_path
from api.users.models import User


class File(models.Model):
    file = models.FileField(
        upload_to=file_generate_upload_path,
        blank=True,
        null=True,
    )

    original_file_name = models.TextField()

    file_name = models.CharField(max_length=256, unique=True)
    file_type = models.CharField(max_length=256)

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="files",
    )

    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        """
        A valid file has the 'upload_finished_at'
        set to a value (not null)
        """
        return bool(self.upload_finished_at)

    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.S3:
            return self.file.url

        return f"{settings.APP_DOMAIN}{self.file.url}"
