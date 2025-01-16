import logging
from datetime import datetime, time
from django.http import JsonResponse

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

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """
        Middleware initialization. Called only once when the server starts.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware logic executed for each request.
        Restricts access to chats outside 6 PM to 9 PM.
        """
        # Define the restricted hours
        start_time = time(21, 0)  # 9 PM
        end_time = time(18, 0)   # 6 PM

        # Get the current server time
        current_time = datetime.now().time()

        # Check if the current time is outside the allowed range
        if not (end_time <= current_time <= start_time):
            return JsonResponse(
                {
                    "error": "Access to the chat is restricted outside 9 PM and 6 PM."
                },
                status=403
            )

        # Proceed with the request if time is allowed
        response = self.get_response(request)
        return response
