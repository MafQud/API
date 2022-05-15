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
    gov: int,
    city: int,
) -> Location:

    # Fetch Governorate & City
    gov = Governorate.objects.get(pk=gov)
    city = City.objects.get(pk=city)

    # Pack location data for validation
    location = Location(lon=lon, lat=lat, address=address, gov=gov, city=city)

    # Data validation
    location.full_clean()

    # Save location instance to the database
    location.save()

    return location


def update_location(
    *,
    location: Location,
    data: Dict,
) -> Location:

    # Fetch Governorate & City if given
    gov_id, city_id = data.get("gov"), data.get("city")

    if gov_id:
        data["gov"] = get_object_or_404(Governorate, pk=gov_id)
    if city_id:
        data["city"] = get_object_or_404(City, pk=city_id)

    non_side_effect_fields = ["lon", "lat", "address", "gov", "city"]

    location, _ = model_update(
        instance=location,
        fields=non_side_effect_fields,
        data=data,
    )

    return location
