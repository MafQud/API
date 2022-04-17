from typing import Dict

from dj_rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..locations.models import City, Governorate
from ..locations.services import create_location
from ..users.models import User
from ..users.services import create_user


class RegisterSerializer(RegisterSerializer):
    password2 = None

    full_name = serializers.CharField()
    gov_id = serializers.IntegerField(write_only=True)
    city_id = serializers.IntegerField(write_only=True)
    firebase_token = serializers.CharField(write_only=True)

    def validate(self, data: Dict):
        return data

    def validate_gov_id(self, id: int) -> int:
        if not Governorate.objects.filter(pk=id).exists():
            raise serializers.ValidationError(_("Invalid governorate id"))

        return id

    def validate_city_id(self, id: int) -> int:
        if not City.objects.filter(pk=id).exists():
            raise serializers.ValidationError(_("Invalid city id"))

        return id

    def save(self) -> User:
        gov = Governorate.objects.get(pk=self.validated_data["gov_id"])
        city = City.objects.get(pk=self.validated_data["city_id"])

        location = create_location(gov=gov, city=city)

        user = create_user(
            username=self.validated_data["username"],
            password=self.validated_data["password"],
            full_name=self.validated_data["full_name"],
            email=self.validated_data["email"],
            firebase_token=self.validated_data["firebase_token"],
            location=location,
        )

        return user
