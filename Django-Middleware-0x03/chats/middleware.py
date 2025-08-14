from datetime import datetime, time
from django.http import HttpResponseForbidden
import logging
from collections import defaultdict
from django.utils.timezone import now


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
            # now = time(20, 0)  # simulate 11 PM
            allowed_start = time(6, 0)
            allowed_end = time(21, 0)

            if not (allowed_start <= now <= allowed_end):
                return HttpResponseForbidden("Access to chats is only allowed between 6AM and 9PM.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store message timestamps by IP
        self.message_log = defaultdict(list)
        self.limit = 5          # messages
        self.time_window = 60   # seconds

    def __call__(self, request):
        # Only track POST requests to the message endpoint
        if request.method == "POST" and request.path.startswith("/chat/messages"):
            ip = self.get_client_ip(request)
            current_time = time.time()

            self.message_log[ip] = [
                t for t in self.message_log[ip]
                if current_time - t <= self.time_window
            ]

            if len(self.message_log[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Message limit exceeded. Please wait before sending more messages."
                )

            # Log this message timestamp
            self.message_log[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip