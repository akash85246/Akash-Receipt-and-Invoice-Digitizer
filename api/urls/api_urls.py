from django.urls import path
from api.views.receipt_views import ReceiptView
from api.views.auth_views import GoogleAuthView
from api.views.auth_views import MeView
from api.views.auth_views import CheckAuthView
from api.views.document_views import UploadDocumentView
from api.views.document_views import DocumentListView
from api.views.document_views import DocumentDetailView

urlpatterns = [
    path("receipts/", ReceiptView.as_view(), name="receipts"),
    path("auth/google/", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/me", MeView.as_view(), name="auth-me"),
    path("api/auth/check", MeView.as_view(), name="auth-check"),
    path("documents/upload", UploadDocumentView.as_view(), name="upload-document"),
    path("documents/history", DocumentListView.as_view(), name="document-list"),
    path("documents/<int:id>/", DocumentDetailView.as_view(), name="document-detail"),
]
