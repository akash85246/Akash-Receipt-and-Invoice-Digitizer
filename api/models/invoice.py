# api/models/invoice.py
from django.db import models
from api.models.base_document import BaseDocument

class Invoice(BaseDocument):
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice - {self.invoice_number or self.id}"