from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from api.models.user import User
from api.utils.google_auth import verify_google_token
from rest_framework.permissions import AllowAny


class GoogleAuthView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Google token missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = verify_google_token(token)
        if not data:
            return Response(
                {"error": "Invalid Google token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user, _ = User.objects.get_or_create(
            google_id=data["google_id"],
            defaults={
                "email": data["email"],
                "username": data["email"],
                "first_name": data["full_name"],
                "avatar": data["picture"],
                "access_token": token
            }
        )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "avatar": user.avatar,
            },
            "access": access_token
        })
        
        #  HttpOnly cookies 
        response.set_cookie(
            key="access",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
        )
        # Refresh token cookie
        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
        )

        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar,
        })


class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"message": "User is authenticated"}, user,
                        status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"message": "Logout successful"}, status=200)

        response.delete_cookie("access", path="/")
        response.delete_cookie("refresh", path="/")

        return response