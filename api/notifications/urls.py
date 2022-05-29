from django.urls import path

from api.notifications.apis import NotificationListApi, NotificationReadApi

app_name = "notifications"
urlpatterns = [
    path("", NotificationListApi.as_view(), name="notification_list"),
    path(
        "<int:notification_id>/read/",
        NotificationReadApi.as_view(),
        name="notification_read",
    ),
]
