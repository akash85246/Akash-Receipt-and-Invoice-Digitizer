# api/models/invoice.py
from django.db import models
from django.conf import settings
from api.models.base_document import BaseDocument

class Invoice(BaseDocument):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice - {self.invoice_number or self.id}"