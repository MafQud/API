from django.urls import path

from api.notifications.apis import NotificationListApi

app_name = "notifications"
urlpatterns = [
    path("", NotificationListApi.as_view(), name="notification_list"),
]
