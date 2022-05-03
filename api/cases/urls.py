from django.urls import path

from .apis import CaseListApi, CreateCaseApi, DetailsCaseApi

app_name = "cases"

urlpatterns = [
    path("", CaseListApi.as_view(), name="list"),
    path("<int:case_id>/", DetailsCaseApi.as_view(), name="detail"),
    path("create/", CreateCaseApi.as_view(), name="create"),
    # path("<int:case_id>/update/", UpdateCaseApi.as_view(), name="update"),
]
