"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import api.routing
from api.middleware import CookieJWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.setup()

application = ProtocolTypeRouter(
    {
        # HTTP requests
        "http": get_asgi_application(),

        # WebSocket requests
        "websocket": CookieJWTAuthMiddleware( 
            AuthMiddlewareStack(
                URLRouter(
                    api.routing.websocket_urlpatterns
                )
            )
        ),
    }
)
