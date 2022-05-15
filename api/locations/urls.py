from django.urls import path

from .apis import GovernorateCitiesListApi, GovernorateListApi

app_name = "locations"

urlpatterns = [
    path("governorates/", GovernorateListApi.as_view(), name="Governorates"),
    path(
        "governorates/<int:gov_id>/cities",
        GovernorateCitiesListApi.as_view(),
        name="Governorate_cities",
    ),
]
