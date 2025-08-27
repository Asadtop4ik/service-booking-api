from http import HTTPStatus

from django.http import JsonResponse

from apps.core.utils.format import format_error_response

from .exception_constants import ErrorTypes


class ProcessExceptions:
    """
    Middleware for processing exceptions and returning a JSON response.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response function.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Called for each request before the view is called.
        """
        return self.get_response(request)

    def process_exception(self, request, exception):
        """
        Process exceptions raised during the request and return a JSON response.
        """
        # Use a utility function to format the error response
        formatted_response, status_code = format_error_response(
            exception_instance=exception, error_type=ErrorTypes.SERVER_ERROR
        )
        if status_code != HTTPStatus.INTERNAL_SERVER_ERROR:
            return JsonResponse(formatted_response, status=status_code)
        return None
