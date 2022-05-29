from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from api.notifications.models import Notification
from api.users.models import User


def list_user_notification(*, user: User) -> QuerySet[Notification]:
    return user.notifications.all()


def get_notification(*, pk: int, fetched_by: User) -> Notification:
    notification = get_object_or_404(Notification, pk=pk)

    if not notification.sent_to == fetched_by:
        raise PermissionDenied()

    return notification
