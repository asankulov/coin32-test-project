from django.utils.deprecation import MiddlewareMixin


class CustomSessionMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def process_request(self, request):
        if request.session.session_key is None:
            request.session.cycle_key()
