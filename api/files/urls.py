from django.urls import include, path

from api.files.views import (
    FileDirectUploadFinishApi,
    FileDirectUploadLocalApi,
    FileDirectUploadStartApi,
    FileStandardUploadApi,
)

app_name = "files"
urlpatterns = [
    path(
        "upload/",
        include(
            (
                [
                    path("standard/", FileStandardUploadApi.as_view(), name="standard"),
                    path(
                        "direct/",
                        include(
                            (
                                [
                                    path(
                                        "start/",
                                        FileDirectUploadStartApi.as_view(),
                                        name="start",
                                    ),
                                    path(
                                        "finish/",
                                        FileDirectUploadFinishApi.as_view(),
                                        name="finish",
                                    ),
                                    path(
                                        "local/<str:file_id>/",
                                        FileDirectUploadLocalApi.as_view(),
                                        name="local",
                                    ),
                                ],
                                "direct",
                            )
                        ),
                    ),
                ],
                "upload",
            )
        ),
    )
]
