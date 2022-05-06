from django.contrib import admin

from api.notifications.models import Notification


@admin.register(Notification)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "level", "sent_to")
    list_filter = ("level",)
