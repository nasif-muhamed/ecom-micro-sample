import logging

logger = logging.getLogger(__name__)

class LogRequestHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the Host header and the full request headers
        logger.info(f"Request Host: {request.META.get('HTTP_HOST')}")
        logger.info(f"Full Request Headers: {request.META}")

        # Proceed with the request
        response = self.get_response(request)
        return response
