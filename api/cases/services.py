from datetime import date
from typing import Dict, List, Optional

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from api.common.utils import get_object
from api.files.models import File
from api.locations.models import Location
from api.locations.services import create_location
from api.notifications.models import Notification
from api.notifications.services import create_notification
from api.users.models import User

from .models import Case, CaseContact, CaseDetails, CaseMatch, CasePhoto

# from fcm_django.models import FCMDevice
# from firebase_admin.messaging import Message
# from firebase_admin.messaging import Notification as FirebaseNotification

Gender = CaseDetails.Gender
CaseType = Case.Types


def create_case_photo(*, case: Case, file: File) -> CasePhoto:
    photo = CasePhoto(case=case, file=file)
    photo.full_clean()
    photo.save()

    return photo


@transaction.atomic
def create_case(
    *,
    type: CaseType,
    user: User,
    location: Dict,
    thumbnail: int,
    file_ids: List[int],
    details: Optional[Dict] = {},
) -> Case:

    # Fetch & create case related objects
    location: Location = create_location(**location)
    thumbnail = get_object(File, pk=thumbnail)

    if not thumbnail:
        raise ValidationError("Invalid Thumbnail file id")

    case = Case(type=type.upper(), user=user, location=location, thumbnail=thumbnail)

    case.full_clean()
    case.save()

    files = File.objects.filter(id__in=file_ids)

    if not files:
        raise ValidationError("Invalid files ids")

    for file in files:
        create_case_photo(case=case, file=file)

    create_case_details(case=case, **details)

    # TODO Factor out to an async function
    activate_case(case)
    case.save()

    return case


def update_case():
    ...


def create_case_details(
    *,
    case: Case,
    name: Optional[str] = None,
    gender: Gender = Gender.UNKNOWN,
    age: Optional[int] = None,
    last_seen: Optional[date] = None,
    description: Optional[str] = None,
    location: Optional[Dict] = None,
) -> CaseDetails:
    loc = None
    if location:
        loc: Location = create_location(**location)

    case_details = CaseDetails(
        case=case,
        name=name,
        gender=gender,
        age=age,
        last_seen=last_seen,
        description=description,
        location=loc,
    )

    case_details.full_clean()
    case_details.save()

    return case_details


def create_case_match(*, missing: Case, found: Case, score: int) -> CaseMatch:
    case_match = CaseMatch(missing=missing, found=found, score=score)
    case_match.full_clean()
    case_match.save()

    return case_match


def process_case(case: Case) -> List[Dict[int, int]]:
    """
    Send case id and photos to the machine learing model then
    recives list of ids & scores that matched with the case
    """
    return []


def case_matching_binding(*, case: Case, matches_list: List[Dict[int, int]]) -> None:
    """ """
    if not matches_list:
        create_notification(
            case=case,
            action=Notification.Action.PUBLISH,
            title="لم نجد حالات مشابه هل تود فى نشر الحاله",
            body="لم نعثر على اى حالات مشابهه يمكنك نشر بيانات المفقود فى نطاق اوسع لتزيد احتماليه العثور عليه",
            level=Notification.Level.WARNING,
            sent_to=case.user,
        )
        return

    cases_ids = [match["id"] for match in matches_list]
    cases_scores = [match["score"] for match in matches_list]
    matches: List[Case] = Case.objects.filter(id__in=cases_ids)

    missing = True if case.type == CaseType.MISSING else False

    for match, score in zip(matches, cases_scores):
        if missing:
            create_case_match(missing=case, found=match, score=score)
        else:
            create_case_match(missing=match, found=case, score=score)

        create_notification(
            case=match,
            action=Notification.Action.MATCHES,
            title="تم العثور على حالات مشابه",
            body="تم الوصول لبعض النتائج قم بتصفحها الان",
            level=Notification.Level.SUCCESS,
            sent_to=match.user,
        )

    create_notification(
        case=case,
        action=Notification.Action.MATCHES,
        title="تم العثور على حالات مشابه",
        body="تم الوصول لبعض النتائج قم بتصفحها الان",
        level=Notification.Level.SUCCESS,
        sent_to=case.user,
    )


def activate_case(case: Case):
    matches = process_case(case)
    case_matching_binding(case=case, matches_list=matches)
    case.activate()
    # TODO success or failure notification
    create_notification(
        case=case,
        action=Notification.Action.DETAILS,
        title="تم رفع الحاله بنجاح",
        body="جارى البحث عن المفقود وسنقوم بإشعارك فى حاله العثور لأى نتائج",
        level=Notification.Level.INFO,
        sent_to=case.user,
    )

    # msg = Message(
    #     notification=FirebaseNotification(
    #         title="تم رفع الحاله بنجاح",
    #         body="جارى البحث عن المفقود وسنقوم بإشعارك فى حاله العثور لأى نتائج",
    #     )
    # )

    # case.user.fcmdevice.send_message(msg)


def publish_case(*, case: Case, performed_by: User):
    if case.user != performed_by:
        raise PermissionDenied()

    if not case.is_active:
        raise ValidationError("Cannot publish inactive case")

    if case.posted_at:
        raise ValidationError("Case already published")

    case.publish()
    case.save()

    create_notification(
        case=case,
        action=Notification.Action.DETAILS,
        title="تم نشر الحاله بنجاح",
        body="تم نشر بيانات المعثور عليه بنجاح انتظر منا اشعار اخر فى حين الوصول لأى نتائج",
        level=Notification.Level.SUCCESS,
        sent_to=case.user,
    )

    # msg = Message(
    #     notification=FirebaseNotification(
    #         title="تم نشر الحاله بنجاح",
    #         body="تم نشر بيانات المعثور عليه بنجاح انتظر منا اشعار اخر فى حين الوصول لأى نتائج",
    #     )
    # )
    # device = FCMDevice.objects.filter(user=case.user).first()
    # device.send_message(msg)


def create_case_contact(*, user: User, case: Case) -> CaseContact:
    contact = CaseContact(case=case, user=user)
    contact.full_clean()
    contact.save()

    return contact


@transaction.atomic
def update_case_contact(contact: CaseContact) -> None:
    contact.answered_at = timezone.now()
    contact.case.finish()

    contact.case.save()
    contact.save()
