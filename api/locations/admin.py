from django.contrib import admin

from .models import City, Governorate, Location


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en", "gov")
    list_filter = ("gov",)
    search_fields = ("name_en", "name_ar")


@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    list_display = ("name_ar", "name_en")
    search_fields = ("name_en", "name_ar")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("lon", "lat", "address", "gov", "city")
    list_filter = ("gov", "city")
    search_fields = ("address",)
