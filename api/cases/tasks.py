from api.cases.models import Case
from api.common.utils import get_object
from config import celery_app


@celery_app.task
def activate_case(case_id: int):
    from api.cases.services import case_matching_binding, process_case

    case = get_object(Case, pk=case_id)
    matches = process_case(case)
    case_matching_binding(case=case, matches=matches)
    case.activate()
    case.save()
