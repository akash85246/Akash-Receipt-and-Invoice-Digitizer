from django.db import models

class OCRMetadata(models.Model):
    ENGINE_CHOICES = [
        ("tesseract", "Tesseract"),
        ("paddle", "PaddleOCR"),
        ("google", "Google Vision"),
    ]

    engine_used = models.CharField(max_length=50, choices=ENGINE_CHOICES)
    confidence_score = models.FloatField(blank=True, null=True)

    raw_response = models.JSONField(
        help_text="Raw OCR JSON output",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)