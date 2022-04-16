from django.db import models


class City(models.Model):
    name_ar = models.CharField(max_length=64)
    name_en = models.CharField(max_length=64)
    gov = models.ForeignKey(on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name_en


class Governorate(models.Model):
    name_ar = models.CharField(max_length=64)
    name_en = models.CharField(max_length=64)

    def __str__(self):
        return self.name_en


class Location(models.Model):
    lon = models.DecimalField()
    lat = models.DecimalField()
    address = models.CharField(max_length=512, blank=True)

    class Meta:
        db_table = "locations"
        verbose_name = "location"
        verbose_name_plural = "locations"
