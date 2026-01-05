from rest_framework import serializers

class BaseDocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()
    extracted_text = serializers.CharField(allow_blank=True, required=False)
    merchant_name = serializers.CharField(allow_null=True, required=False)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, allow_null=True, required=False
    )
    date = serializers.DateField(allow_null=True, required=False)
    category = serializers.CharField(allow_null=True, required=False)
    created_at = serializers.DateTimeField()