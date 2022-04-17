from datetime import date
from typing import Dict, List, Optional

from django.db import transaction

from api.users.models import User

from .models import Case, CaseDetails, CaseMatch, CasePhoto

Gender = CaseDetails.Gender
CaseType = Case.Types


def create_case_photo(*, case: Case, url: str) -> CasePhoto:
    photo = CasePhoto(case=case, url=url)
    photo.full_clean()
    photo.save()

    return photo


@transaction.atomic
def create_case(*, type: CaseType, user: User, photos_urls: List[str]) -> Case:
    case = Case(type=type, user=user)
    case.full_clean()
    case.save()

    for url in photos_urls:
        create_case_photo(case=case, url=url)

    return case


def create_case_details(
    *,
    case: Case,
    name: Optional[str] = None,
    gender: Gender = Gender.UNKNOWN,
    age: Optional[int] = None,
    last_seen: Optional[date] = None,
    description: Optional[str] = None,
) -> CaseDetails:

    case_details = CaseDetails(
        case=case,
        name=name,
        gender=gender,
        age=age,
        last_seen=last_seen,
        description=description,
    )

    case_details.full_clean()
    case_details.save()

    return case_details


def create_case_match(*, missing: Case, found: Case, score: int) -> CaseMatch:
    case_match = CaseMatch(missing=missing, found=found, score=score)
    case_match.full_clean()
    case_match.save()

    return case_match


def process_case(*, case: Case) -> List[Dict[int, int]]:
    """
    Send case id and photos to the machine learing model then
    recives list of ids & scores that matched with the case
    """
    ...


def case_matching_binding(*, case: Case, matches_list: List[Dict[int, int]]) -> None:
    """
    Bind the processed case with it's matches by instaniating CaseMatch objects
    """
    cases_ids = [match["id"] for match in matches_list]
    cases_scores = [match["score"] for match in matches_list]
    matches: List[Case] = Case.objects.filter(id__in=cases_ids)
    if not matches:
        return

    missing = True if case.type == CaseType.MISSING else False

    for match, score in zip(matches, cases_scores):
        if missing:
            create_case_match(missing=case, found=match, score=score)
        else:
            create_case_match(missing=match, found=case, score=score)
