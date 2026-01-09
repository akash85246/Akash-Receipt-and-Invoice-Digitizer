from django.urls import re_path
from api.consumers.upload_progress import UploadProgressConsumer

websocket_urlpatterns = [
    re_path(r"ws/upload-progress/$", UploadProgressConsumer.as_asgi()),
]