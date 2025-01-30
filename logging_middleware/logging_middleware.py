"""Middleware to log exceptions to the console."""

import traceback

from django.http import JsonResponse

from .utils import log_message_jsonl


class JsonLoggingMiddleware:
    """Middleware to log all requests, responses, and exceptions."""

    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call the middleware."""
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request):
        """Log incoming requests."""
        request_data = {
            "method": request.method,
            "path": request.path,
            "GET": request.GET.dict(),
            "POST": request.POST.dict(),
            "body": request.body.decode() if request.headers.get("content-type") == "application/json" else "",
        }
        log_message_jsonl("INFO", "Incoming request", **request_data)

    def process_response(self, request, response):
        """Log outgoing responses."""
        response_data = {
            "status_code": response.status_code,
            "reason_phrase": response.reason_phrase,
            "content": response.content.decode("utf-8") if hasattr(response, "content") else "",
        }
        log_message_jsonl("INFO", "Outgoing response", **response_data)
        return response

    def process_exception(self, request, exception):
        """Log exceptions."""
        exception_data = {
            "exception": str(exception),
            "path": request.path,
            "stacktrace": traceback.format_exc(),
        }
        log_message_jsonl("ERROR", "Exception occurred", **exception_data)
        response_data = {"error": "An internal server error occurred. Please try again later."}
        return JsonResponse(response_data, status=500)
