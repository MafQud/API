from django.contrib import admin

from .models import Case, CaseDetails, CaseMatch, CasePhoto

admin.site.register((Case, CaseDetails, CaseMatch, CasePhoto))
