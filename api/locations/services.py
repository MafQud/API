from pathlib import Path

from .models import City, Governorate
from .utils import read_json

cwd = Path.cwd


def populate_govs() -> None:
    """
    Populates governorates and cities tables
    """
    # Read json files
    govs_dict = read_json(cwd / "govs.json")
    cities_dict = read_json(cwd / "cities.json")

    # Reset tables
    Governorate.objects.all().delete()
    City.objects.all().delete()

    # Insert govs
    for gov in govs_dict["data"]:
        g = Governorate(
            pk=gov["id"],
            name_ar=gov["governorate_name_ar"],
            name_en=gov["governorate_name_en"],
        )
        g.save()

        # Insert cities in gov
        for city in cities_dict["data"][gov["id"]]:
            c = City(
                pk=city["id"],
                name_ar=city["city_name_ar"],
                name_en=city["city_name_en"],
            )
            c.save()
