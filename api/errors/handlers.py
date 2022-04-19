from typing import Dict

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


def custom_exception_handler(exc: Exception, ctx: Dict) -> Response:
    """
    {
        "status_code": 4xx/5xx,
        "message": "Error message"
        "detail": {
            "field": ["Error message"]
        }
    }
    """
    # Handle django exceptions
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    elif isinstance(exc, Http404):
        exc = exceptions.NotFound()

    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    # Call the default drf exception handler
    response = exception_handler(exc, ctx)

    # Raise 500 in case of unexpected error
    if response is None:
        return response

    response_body = {}
    if isinstance(exc.detail, (list, dict)):
        response_body["detail"] = response.data
        response_body["message"] = "Validation error"
    else:
        response_body["detail"] = {}
        response_body["message"] = exc.detail

    response_body["status_code"] = response.status_code
    response.data = response_body

    return response
