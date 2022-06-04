from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from api.cases.tasks import activate_case
from api.common.utils import get_object
from api.files.models import File
from api.integrations.ai.model import AIModel
from api.locations.models import Location
from api.locations.services import create_location
from api.notifications.models import Notification
from api.notifications.services import create_notification
from api.users.models import User

from .models import Case, CaseContact, CaseDetails, CaseMatch, CasePhoto, PhotoEncoding

# from fcm_django.models import FCMDevice
# from firebase_admin.messaging import Message
# from firebase_admin.messaging import Notification as FirebaseNotification

Gender = CaseDetails.Gender
CaseType = Case.Types
ml_model = None


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

    create_notification(
        case=case,
        action=Notification.Action.DETAILS,
        title="تم رفع الحاله بنجاح",
        body="جارى البحث عن المفقود وسنقوم بإشعارك فى حاله العثور لأى نتائج",
        level=Notification.Level.INFO,
        sent_to=case.user,
    )

    case.save()

    activate_case.delay(case.id)

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


def create_photo_encoding(*, photo: CasePhoto, values: List[float]):
    photo_encoding = PhotoEncoding(photo=photo, values=values)
    photo_encoding.full_clean()
    photo_encoding.save()

    return photo_encoding


def process_case(case: Case) -> Dict[int, float]:
    """
    Send case photos to the machine learning model to find it's matches
    """

    # Instantiate the model
    global ml_model
    if ml_model is None:
        all_encodings = PhotoEncoding.objects.all()

        encodings_data = ()
        encodings_labels = ()

        for photo_encoding in all_encodings:
            encodings_data, encodings_labels = zip(
                *[
                    (photo_encoding.values, photo_encoding.photo.case.id)
                    for photo_encoding in all_encodings
                ]
            )

        ml_model = AIModel(
            facenet_path=settings.APPS_DIR / "integrations/ai/facenet_keras.h5",
            knn_path=settings.APPS_DIR / "integrations/ai/knn_new.clf",
            data=np.asarray(encodings_data),
            labels=np.asarray(encodings_labels),
        )

    matches = {}
    new_photos_encodings = []
    valid_photos = 0
    # Fetch all case photos
    photos = case.photos.all()

    # Test each photo in the case against our ML model
    for photo in photos:
        # Extract face encoding
        encoding = ml_model.encode_photo(photo.file.url)
        if not encoding:
            continue
        valid_photos += 1
        # Record encoding to the database
        photo_encoding = create_photo_encoding(photo=photo, values=encoding)
        # Temporary storing new encoding to train the model at the end
        new_photos_encodings.append(photo_encoding)
        # Run the model against our new encoding to find case matches
        case_ids = ml_model.check_face_identity(photo_encoding)

        # Record matches and their scores
        for case_id in case_ids:
            # Fetch case
            match = get_object(Case, pk=case_id)

            # Safety check if case still exists or not
            if match is None:
                continue

            matches[match] = matches.get(match, 0) + case_ids[case_id]

    # Checks all photos are invalid
    if not valid_photos:
        return {}

    # Normalizing matches scores
    for match in matches:
        matches[match] = matches[match] / valid_photos

    # Add new case photo encodings to the model training data
    new_case_encodings_data = [
        photo_encoding.values for photo_encoding in new_photos_encodings
    ]

    # Retrain the model on the new data
    ml_model.retrain_model(new_case_encodings_data, case.id, Path("api/common"))

    return matches


def case_matching_binding(*, case: Case, matches: Dict[int, int]) -> None:
    """
    Bind the processed case with it's matches by instantiating CaseMatch objects
    """
    if not matches:
        create_notification(
            case=case,
            action=Notification.Action.PUBLISH,
            title="لم نجد حالات مشابه هل تود فى نشر الحاله",
            body="لم نعثر على اى حالات مشابهه يمكنك نشر بيانات المفقود فى نطاق اوسع لتزيد احتماليه العثور عليه",
            level=Notification.Level.WARNING,
            sent_to=case.user,
        )
        return

    missing = True if case.type == CaseType.MISSING else False

    for match, score in matches.items():
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
