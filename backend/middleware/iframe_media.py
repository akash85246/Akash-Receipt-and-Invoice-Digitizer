class MediaIframeMiddleware:
    """
    Allows media files (PDF/images) to be embedded in iframes
    without weakening security for the rest of the app.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith("/media/"):
            # REMOVE iframe blocking headers
            response.headers.pop("X-Frame-Options", None)
            response.headers["Content-Security-Policy"] = "frame-ancestors *"

        return response