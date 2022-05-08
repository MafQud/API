from api.notifications.models import Notification
from api.users.models import User


def list_notification(*, user: User):
    return Notification.objects.filter(sent_to=user)
