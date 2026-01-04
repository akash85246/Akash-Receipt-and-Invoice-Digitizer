from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

from api.models.user import User
from api.utils.google_auth import verify_google_token


class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response({"error": "Token missing"}, status=400)

        data = verify_google_token(token)
        if not data:
            return Response({"error": "Invalid Google token"}, status=401)

        base_username = (
            data["full_name"]
            .lower()
            .replace(" ", "_")
        )

        username = base_username
        if User.objects.filter(username=username).exists():
            username = f"{base_username}_{uuid.uuid4().hex[:6]}"

        user, created = User.objects.get_or_create(
            google_id=data["google_id"],
            defaults={
                "email": data["email"],
                "username": username,
                "first_name": data["full_name"],
                "avatar": data["picture"],
            }
        )

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar": user.avatar,
                "new_user": created,
            }
        }, status=200
        )
