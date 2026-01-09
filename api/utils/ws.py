from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_upload_event(user_id: int, step: str, message: str, progress: int):
    channel_layer = get_channel_layer()
    
    if not channel_layer:
        return 
    
    async_to_sync(channel_layer.group_send)(
        f"upload_{user_id}",
        {
            "type": "upload_message",
            "data": {
                "step": step,
                "message": message,
                "progress": progress,
            },
        },
    )
