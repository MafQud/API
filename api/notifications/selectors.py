from api.users.models import User


def list_user_notification(*, user: User):
    return user.notifications.all()
