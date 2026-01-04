from django.utils.timezone import now

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = now()

        response = self.get_response(request)

        duration = (now() - start_time).total_seconds()
        print(
            f"[{request.method}] {request.path} - {duration:.3f}s"
        )

        return response