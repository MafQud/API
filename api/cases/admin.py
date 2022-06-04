from django.contrib import admin

from .models import Case, CaseContact, CaseDetails, CaseMatch, CasePhoto, PhotoEncoding

admin.site.register(
    (Case, CaseDetails, CaseMatch, CasePhoto, PhotoEncoding, CaseContact)
)
