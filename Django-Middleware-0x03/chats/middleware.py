from datetime import datetime
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