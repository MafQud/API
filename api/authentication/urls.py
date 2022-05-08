from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.authentication.apis import ValidateEmailAPI, ValidatePhoneAPI

app_name = "auth"
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify_token"),
    path("phone/validate/", ValidatePhoneAPI.as_view(), name="validate_phone"),
    path("email/validate/", ValidateEmailAPI.as_view(), name="validate_email"),
]
