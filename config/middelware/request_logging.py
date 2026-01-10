import time
import uuid
import logging

logger = logging.getLogger("api.request")

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        start_time =  time.monotonic()
