from django.urls import path

from .apis import (
    CaseArchiveApi,
    CaseContactCreateApi,
    CaseContactUpdateApi,
    CaseFinishApi,
    CaseListApi,
    CaseMatchListApi,
    CasePublishApi,
    CreateCaseApi,
    DetailsCaseApi,
)

app_name = "cases"

urlpatterns = [
    path("", CaseListApi.as_view(), name="list"),
    path("<int:case_id>/", DetailsCaseApi.as_view(), name="detail"),
    path("create/", CreateCaseApi.as_view(), name="create"),
    path("contacts/create/", CaseContactCreateApi.as_view(), name="create_contact"),
    path(
        "contacts/<int:case_contact_id>/update/",
        CaseContactUpdateApi.as_view(),
        name="update_contact",
    ),
    # path("<int:case_id>/update/", UpdateCaseApi.as_view(), name="update"),
    path("<int:case_id>/matches/", CaseMatchListApi.as_view(), name="matches"),
    path("<int:case_id>/publish/", CasePublishApi.as_view(), name="publish"),
    path("<int:case_id>/finish/", CaseFinishApi.as_view(), name="finish"),
    path("<int:case_id>/archive/", CaseArchiveApi.as_view(), name="archive"),
]
