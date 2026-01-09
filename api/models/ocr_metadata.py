# api/models/ocr_metadata.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class OCRMetadata(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="ocr_metadata"
    )
    object_id = models.PositiveIntegerField()
    document = GenericForeignKey("content_type", "object_id")
    engine_used = models.CharField(
        max_length=50,
        choices=[
            ("tesseract", "Tesseract"),
            ("paddle", "PaddleOCR"),
            ("google", "Google Vision"),
        ]
    )

    confidence_score = models.FloatField(blank=True, null=True)

    raw_response = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OCR ({self.engine_used}) - {self.created_at}"