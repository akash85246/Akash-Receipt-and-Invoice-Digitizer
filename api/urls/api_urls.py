from django.urls import path
from api.views.receipt_views import ReceiptView
from api.views.auth_views import GoogleAuthView

urlpatterns = [
    path("receipts/", ReceiptView.as_view(), name="receipts"),
     path("auth/google/", GoogleAuthView.as_view(), name="google-auth"),
]