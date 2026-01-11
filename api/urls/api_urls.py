from django.urls import path
from api.views.auth_views import RefreshAccessTokenView
from api.views.auth_views import GoogleAuthView
from api.views.auth_views import MeView
from api.views.auth_views import LogoutView
from api.views.document_views import UploadDocumentView
from api.views.document_views import DocumentListView
from api.views.receipt_views import ReceiptDetailView
from api.views.receipt_views import UpdateReceiptView
from api.views.receipt_views import DeleteReceiptView
from api.views.invoice_views import InvoiceDetailView
from api.views.invoice_views import UpdateInvoiceView
from api.views.invoice_views import DeleteInvoiceView
from api.views.document_views import DeleteMultipleDocumentsView

urlpatterns = [
    path("auth/me", MeView.as_view(), name="auth-me"),
    path("auth/refresh/", RefreshAccessTokenView.as_view(), name="token-refresh"),
    path("auth/google/", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/logout", LogoutView.as_view(), name="auth-logout"),
    path("documents/upload", UploadDocumentView.as_view(), name="upload-document"),
    path("documents/history/", DocumentListView.as_view(), name="document-history"),
    path("documents/delete-multiple", DeleteMultipleDocumentsView.as_view(),name="delete-multiple-documents"),
    path("receipt/<int:receipt_id>/", ReceiptDetailView.as_view(), name="receipt-detail"),
    path( "receipt/update/<int:receipt_id>/", UpdateReceiptView.as_view(),name="update-receipt"),
    path("receipt/delete/<int:receipt_id>/", DeleteReceiptView.as_view(), name="delete-receipt"),
    path("invoice/<int:invoice_id>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("invoice/update/<int:invoice_id>/",UpdateInvoiceView.as_view(), name="update-invoice"),
    path("invoice/delete/<int:invoice_id>/", DeleteInvoiceView.as_view(), name="delete-invoice"),
]
