from typing import Dict, Optional

from django.conf import settings
from django.shortcuts import get_object_or_404

from api.common.services import model_update
from api.locations.models import City, Governorate, Location
from api.locations.utils import read_json

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
    gov_id: int,
    city_id: int,
) -> Location:

    gov = Governorate.objects.get(pk=gov_id)
    city = City.objects.get(pk=city_id)
    loc = Location(lon=lon, lat=lat, address=address, gov=gov, city=city)
    loc.full_clean()
    # loc.clean()
    loc.save()

    return loc


def update_location(
    *,
    location_id: int,
    data: Dict,
) -> Location:

    fields = ["lon", "lat", "address", "gov", "city"]
    location = get_object_or_404(Location, id=location_id)

    city_id = data.get("city_id")
    if city_id is not None and city_id != location.city.id:
        city = get_object_or_404(City, city_id)
        gov = get_object_or_404(Governorate, city.gov.id)

        data["gov"] = gov
        data["city"] = city

    location, has_updated = model_update(
        intance=location,
        fields=fields,
        data=data,
    )

    return location
