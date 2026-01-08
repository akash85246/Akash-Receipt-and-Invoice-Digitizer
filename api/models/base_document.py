# api/models/base_document.py
from django.db import models

class BaseDocument(models.Model):
    image = models.ImageField(upload_to="documents/images/")
    extracted_text = models.TextField(blank=True, null=True)
    merchant_name = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    confidence_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expense_type = models.CharField(max_length=100, blank=True, null=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        abstract = True