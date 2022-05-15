from typing import Optional

from fcm_django.models import FCMDevice

from api.notifications.models import Notification
from api.users.models import User


def create_notification(
    *,
    title: str,
    body: str,
    level: str,
    sent_to: User,
) -> Notification:

    notification = Notification(
        title=title,
        body=body,
        level=level,
        sent_to=sent_to,
    )
    notification.full_clean()
    notification.save()

    return notification


def create_fcm_device(
    *,
    user: User,
    fcm_token: str,
    device_type: Optional[str] = "android",
) -> FCMDevice:

    device = FCMDevice(
        user=user,
        type=device_type,
        registration_id=fcm_token,
    )
    device.full_clean()
    device.save()

    return device
