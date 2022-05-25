from django.urls import path

from api.cases.apis import UserCasesListApi
from api.users.apis import CreateUserApi, DetailUserApi, SetNationalIdApi, UpdateUserApi

app_name = "users"
urlpatterns = [
    path("create/", CreateUserApi.as_view(), name="create_user"),
    path("<int:user_id>/", DetailUserApi.as_view(), name="get_user"),
    path("<int:user_id>/update/", UpdateUserApi.as_view(), name="update_user"),
    path("cases/", UserCasesListApi.as_view(), name="get_user_cases"),
    path("<int:user_id>/set/id/", SetNationalIdApi.as_view(), name="set_id"),
]
