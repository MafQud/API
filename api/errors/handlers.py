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

    if isinstance(exc.detail, (list, dict)):
        response.data["detail"] = response.data
        response.data["message"] = "Validation error"
    else:
        response.data["detail"] = {}
        response.data["message"] = exc.detail

    response.data["status_code"] = response.status_code

    return response
