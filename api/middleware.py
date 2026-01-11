from channels.middleware import BaseMiddleware



class CookieJWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.auth import get_user_model
        from rest_framework_simplejwt.tokens import UntypedToken
        from django.conf import settings
        from jwt import decode as jwt_decode

        User = get_user_model()
        headers = dict(scope["headers"])
        cookie_header = headers.get(b"cookie", b"").decode()

        cookies = {}
        for item in cookie_header.split(";"):
            if "=" in item:
                k, v = item.strip().split("=", 1)
                cookies[k] = v

        raw_token = cookies.get("access")

        if raw_token is None:
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            UntypedToken(raw_token) 

            decoded = jwt_decode(
                raw_token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            user = await User.objects.aget(id=decoded["user_id"])
            scope["user"] = user

        except Exception:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)