from rest_framework import serializers
from api.models.invoice import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

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
            "created_at",
        ]

    def get_type(self, obj):
        return "invoice"