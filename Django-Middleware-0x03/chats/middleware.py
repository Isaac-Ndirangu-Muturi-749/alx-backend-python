import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Middleware initialization. Called only once when the server starts.
        """
        self.get_response = get_response
        # Configure the logger
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s",
        )

    def __call__(self, request):
        """
        Middleware logic executed for each request.
        """
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response
