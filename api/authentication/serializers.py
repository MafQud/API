from typing import Dict

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import JWTSerializer
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..locations.models import City, Governorate
from ..locations.services import create_location
from ..users.models import User
from ..users.services import create_user


class RegisterSerializer(RegisterSerializer):
    password1 = None
    password2 = None

    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
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

    def save(self, request: HttpRequest) -> User:
        gov = Governorate.objects.get(pk=self.validated_data["gov_id"])
        city = City.objects.get(pk=self.validated_data["city_id"])

        location = create_location(gov=gov, city=city)

        user = create_user(
            username=self.validated_data.get("username"),
            password=self.validated_data.get("password"),
            name=self.validated_data.get("name"),
            email=self.validated_data.get("email"),
            firebase_token=self.validated_data.get("firebase_token"),
            location=location,
        )

        return user


class JWTSerializer(JWTSerializer):
    ...
