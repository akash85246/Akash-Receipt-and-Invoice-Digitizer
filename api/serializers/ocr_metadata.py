from rest_framework import serializers
from api.models.ocr_metadata import OCRMetadata


class OCRMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRMetadata
        fields = [
            "engine_used",
            "confidence_score",
            "raw_response",
            "created_at",
        ]