import json
from channels.generic.websocket import AsyncWebsocketConsumer


class UploadProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        # Authentication check
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.user = user
        self.group_name = f"upload_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def upload_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))