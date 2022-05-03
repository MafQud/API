from django.urls import include, path

app_name = "apis"
urlpatterns = [
    path("auth/", include("api.authentication.urls", "authentication")),
    path("users/", include("api.users.urls", "users")),
    path("cases/", include("api.cases.urls", "cases")),
    path("files/", include("api.files.urls", "files")),
]
