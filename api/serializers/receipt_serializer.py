from rest_framework import serializers
from api.models.receipt import Receipt
from api.models.items import Item
from api.models.ocr_metadata import OCRMetadata
from .item_serializer import ItemSerializer
from django.contrib.contenttypes.models import ContentType
from api.models.ocr_metadata import OCRMetadata
from api.serializers.ocr_metadata import OCRMetadataSerializer

class ReceiptSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    ocr_metadata = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()  # ✅ FIX

    class Meta:
        model = Receipt
        fields = [
            "id",
            "type",
            "image",
            "extracted_text",
            "merchant_name",
            "total_amount",
            "date",
            "category",
            "payment_mode",
            "created_at",
            "ocr_metadata",
            "receipt_number",
            "gst_number",
            "currency",
            "address",
            "confidence_score",
            "tax_amount",
            "expense_type",
            "items",
            "is_reviewed",
            "processed_image",
        ]

    def get_items(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        items = Item.objects.filter(
            content_type=ct,
            object_id=obj.id
        )
        return ItemSerializer(items, many=True).data

    def get_type(self, obj):
        return "receipt"

    def get_ocr_metadata(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        meta = OCRMetadata.objects.filter(
            content_type=ct,
            object_id=obj.id
        ).order_by("-created_at").first()

        return OCRMetadataSerializer(meta).data if meta else None