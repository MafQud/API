from typing import Optional

from django.conf import settings

from .models import City, Governorate, Location
from .utils import read_json

apps_dir = settings.APPS_DIR


def populate_govs() -> None:
    """
    Populates governorates and cities tables
    """
    # Read json files
    govs_dict = read_json(path=apps_dir / "locations" / "govs.json")
    cities_dict = read_json(path=apps_dir / "locations" / "cities.json")

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
                gov=g,
                pk=city["id"],
                name_ar=city["city_name_ar"],
                name_en=city["city_name_en"],
            )
            c.save()


def create_location(
    *,
    lon: Optional[float] = None,
    lat: Optional[float] = None,
    address: Optional[str] = None,
    gov: Governorate,
    city: City
) -> Location:

    loc = Location(lon=lon, lat=lat, address=address, gov=gov, city=city)
    loc.full_clean()
    loc.save()

    return loc
