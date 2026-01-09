import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer


class UploadProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = None

        try:
            # 🔹 Lazy imports (CRITICAL)
            from django.conf import settings
            from django.contrib.auth import get_user_model
            from rest_framework_simplejwt.backends import TokenBackend

            User = get_user_model()

            query = parse_qs(self.scope["query_string"].decode())
            token = query.get("token", [None])[0]

            if not token:
                await self.close()
                return

            token_backend = TokenBackend(
                algorithm="HS256",
                signing_key=settings.SECRET_KEY,
            )

            payload = token_backend.decode(token, verify=True)
            user_id = payload.get("user_id")

            if not user_id:
                await self.close()
                return

            self.user = await User.objects.aget(id=user_id)

            self.group_name = f"upload_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

        except Exception as e:
            print("WebSocket auth error:", e)
            await self.close()

    async def disconnect(self, close_code):
        if self.group_name:
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name
            )

    async def upload_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))