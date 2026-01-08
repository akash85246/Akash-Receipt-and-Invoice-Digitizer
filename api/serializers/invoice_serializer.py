from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from api.models.invoice import Invoice
from api.models.items import Item
from api.models.ocr_metadata import OCRMetadata

from api.serializers.item_serializer import ItemSerializer
from api.serializers.ocr_metadata import OCRMetadataSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    ocr_metadata = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "type",
            "image",
            "extracted_text",
            "merchant_name",
            "total_amount",
            "date",
            "category",
            "invoice_number",
            "gst_number",
            "is_paid",
            "due_date",
            "currency",
            "address",
            "tax_amount",
            "expense_type",
            "confidence_score",
            "created_at",
            "ocr_metadata",
            "items",
            "is_reviewed",
        ]

    def get_type(self, obj):
        return "invoice"

    def get_items(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        items = Item.objects.filter(
            content_type=ct,
            object_id=obj.id
        )
        return ItemSerializer(items, many=True).data

    def get_ocr_metadata(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        meta = OCRMetadata.objects.filter(
            content_type=ct,
            object_id=obj.id
        ).order_by("-created_at").first()

        return OCRMetadataSerializer(meta).data if meta else None