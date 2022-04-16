from django.db import models


class City(models.Model):
    name_ar = models.CharField(max_length=64)
    name_en = models.CharField(max_length=64)
    gov = models.ForeignKey(on_delete=models.CASCADE, related_name="cities")

    class Meta:
        db_table = "cities"
        verbose_name = "city"
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name_en


class Governorate(models.Model):
    name_ar = models.CharField(max_length=64)
    name_en = models.CharField(max_length=64)

    class Meta:
        db_table = "governorates"
        verbose_name = "governorate"
        verbose_name_plural = "governorates"

    def __str__(self):
        return self.name_en


class Location(models.Model):
    lon = models.DecimalField()
    lat = models.DecimalField()
    address = models.CharField(max_length=512, blank=True)

    gov = models.ForeignKey(Governorate, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    class Meta:
        db_table = "locations"
        verbose_name = "location"
        verbose_name_plural = "locations"

    def __str__(self):
        return f"<Location: {self.gov.name_en}, {self.city.name_en}>"
