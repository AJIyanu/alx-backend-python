from datetime import datetime, time
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger('user_activity')


class RequestLoggingMiddleware:
    """
    Middleware to log request details.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)

        # Call the next middleware or view
        response = self.get_response(request)

        return response




class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/conversations/') or request.path.startswith('/api/messages/'):
            now = datetime.now().time()
            now = time(20, 0)  # simulate 11 PM
            allowed_start = time(6, 0)
            allowed_end = time(21, 0)

            if not (allowed_start <= now <= allowed_end):
                return HttpResponseForbidden("Access to chats is only allowed between 6AM and 9PM.")

        return self.get_response(request)
