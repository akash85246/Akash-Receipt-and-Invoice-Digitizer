from rest_framework import serializers
from api.models.receipt import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

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
        ]

    def get_type(self, obj):
        return "receipt"