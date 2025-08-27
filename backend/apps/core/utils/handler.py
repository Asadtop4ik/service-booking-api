from functools import singledispatch
from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.db.models.deletion import ProtectedError
from django.db.utils import DatabaseError
from django.http import Http404
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
)
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.core.constants import ConstraintNames

from .exception_constants import ErrorLanguageTypes, ErrorTypes
from .exceptions import DomainException
from .format import format_error_response


class ExceptionMapper:
    """Maps exception types to their corresponding domain exceptions and error types."""

    MAPPINGS = {
        (DjangoPermissionDenied, DRFPermissionDenied): (
            DomainException(1003),
            ErrorTypes.DOMAIN_ERROR,
        ),
        (AuthenticationFailed, NotAuthenticated): (
            DomainException(2005),
            ErrorTypes.DOMAIN_ERROR,
        ),
        Http404: (DomainException(1006), ErrorTypes.SERVER_ERROR),
        ProtectedError: (DomainException(1001), ErrorTypes.DOMAIN_ERROR),
    }

    @classmethod
    def get_mapping(cls, exc: Exception) -> tuple[DomainException, str] | None:
        """Get the corresponding domain exception and error type for a given exception."""
        for exc_types, mapping in cls.MAPPINGS.items():
            if isinstance(exc_types, tuple):
                if isinstance(exc, exc_types):
                    return mapping
            elif isinstance(exc, exc_types):
                return mapping
        return None


def get_language_code(request) -> str:
    """Extract and validate the language code from the request."""
    if not request:
        return ErrorLanguageTypes.RU

    lang_code = request.headers.get("Accept-Language")
    valid_languages = {
        ErrorLanguageTypes.RU,
        ErrorLanguageTypes.UZ,
    }

    return lang_code if lang_code in valid_languages else ErrorLanguageTypes.RU


@singledispatch
def handle_specific_exception(
    exc: Exception, lang_code: str, response_data: dict[str, Any] | None = None
) -> Response | None:
    """Default handler for unspecified exception types."""
    return None


@handle_specific_exception.register(DatabaseError)
def handle_database_error(
    exc: DatabaseError, lang_code: str, response_data: dict[str, Any] | None = None
) -> Response | None:
    """Handle database-specific errors and constraints."""
    cause = exc.__cause__
    constraint_name = (
        cause.diag.constraint_name
        if hasattr(cause, "diag") and hasattr(cause.diag, "constraint_name")
        else None
    )

    constraints = ConstraintNames(exc, constraint_name)
    constraint_exception = constraints.get_exception_class()

    if constraint_exception:
        error_response, status_code = format_error_response(
            exception_instance=constraint_exception,
            error_type=ErrorTypes.DOMAIN_ERROR,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)
    return None


@handle_specific_exception.register(APIException)
def handle_api_exception(
    exc: APIException, lang_code: str, response_data: dict[str, Any] | None = None
) -> Response:
    """Handle REST framework API exceptions."""
    if response_data is None:
        response_data = getattr(exc, "detail", str(exc))

    error_response, status_code = format_error_response(
        response_data, lang_code=lang_code
    )
    return Response(error_response, status=status_code)


def handle_exceptions(exc: Exception, context: dict[str, Any]) -> Response | None:
    """
    Enhanced exception handler with improved error mapping and handling.

    Args:
        exc: The caught exception
        context: The exception context

    Returns:
        Response object with formatted error details or None
    """
    response = exception_handler(exc, context)
    lang_code = get_language_code(context.get("request"))

    # Check for mapped exceptions
    mapping = ExceptionMapper.get_mapping(exc)
    if mapping:
        domain_exc, error_type = mapping
        error_response, status_code = format_error_response(
            exception_instance=domain_exc,
            error_type=error_type,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)

    # Handle domain exceptions
    if isinstance(exc, DomainException):
        error_response, status_code = format_error_response(
            exception_instance=exc,
            error_type=ErrorTypes.DOMAIN_ERROR,
            lang_code=lang_code,
        )
        return Response(error_response, status=status_code)

    # Handle specific exceptions using single dispatch
    response_data = response.data if response else None
    specific_handler_response = handle_specific_exception(exc, lang_code, response_data)
    if specific_handler_response:
        return specific_handler_response

    return response
