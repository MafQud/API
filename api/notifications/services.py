from typing import Optional

from fcm_django.models import FCMDevice

from api.cases.models import Case
from api.notifications.models import Notification
from api.users.models import User


def create_notification(
    *,
    case: Case,
    title: str,
    body: str,
    level: str,
    sent_to: User,
    action: Notification.Action,
) -> Notification:

    notification = Notification(
        case=case,
        title=title,
        body=body,
        level=level,
        sent_to=sent_to,
        action=action,
    )
    notification.full_clean()
    notification.save()

    return notification


def create_fcm_device(
    *,
    user: User,
    firebase_token: str,
    device_type: Optional[str] = "android",
) -> FCMDevice:

    device = FCMDevice(
        user=user,
        type=device_type,
        registration_id=firebase_token,
    )
    device.full_clean()
    device.save()

    return device
