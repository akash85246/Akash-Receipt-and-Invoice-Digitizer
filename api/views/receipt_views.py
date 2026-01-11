from decimal import Decimal
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.serializers.receipt_serializer import ReceiptSerializer
from api.models.receipt import Receipt
from api.models.items import Item

class UpdateReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, receipt_id):
        try:
            receipt = Receipt.objects.get(
                id=receipt_id,
                user=request.user
            )
        except Receipt.DoesNotExist:
            return Response(
                {"error": "Receipt not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data 

        with transaction.atomic():
            allowed_fields = [
                "merchant_name",
                "total_amount",
                "date",
                "category",
                "payment_mode",
                "receipt_number",
                "gst_number",
                "currency",
                "address",
                "tax_amount",
                "expense_type",
                "is_reviewed",
            ]

            for field in allowed_fields:
                if field in data:
                    setattr(receipt, field, data[field])

            receipt.save()


            # Handle items (your logic is correct ✅)
            items_payload = data.get("items", [])
            ct = ContentType.objects.get_for_model(receipt)

            existing_items = {
                item.id: item
                for item in Item.objects.filter(
                    content_type=ct,
                    object_id=receipt.id
                )
            }

            received_item_ids = set()

            for item_data in items_payload:
                item_id = item_data.get("id")
                name = item_data.get("name")
                quantity = int(item_data.get("quantity", 1))
                price = Decimal(item_data.get("price"))
                total_price = price * quantity

                if item_id and item_id in existing_items:
                    item = existing_items[item_id]
                    item.name = name
                    item.quantity = quantity
                    item.price = price
                    item.total_price = total_price
                    item.save()
                    
                else:
                    item = Item.objects.create(
                        content_type=ct,
                        object_id=receipt.id,
                        name=name,
                        quantity=quantity,
                        price=price,
                        total_price=total_price
                    )
                    
                received_item_ids.add(item.id)

            for item_id, item in existing_items.items():
                if item_id not in received_item_ids:
                    item.delete()
        serializer = ReceiptSerializer(receipt)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
            
        
class ReceiptDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, receipt_id):
        try:
            receipt = Receipt.objects.get(id=receipt_id, user=request.user)
            serializer = ReceiptSerializer(receipt)
            return Response(serializer.data, status=200)
        except Receipt.DoesNotExist:
            return Response(
                {"error": "Receipt not found"},
                status=404
            )

class DeleteReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, receipt_id):
        try:
            receipt = Receipt.objects.get(id=receipt_id, user=request.user)
            receipt.delete()
            return Response(
                {"message": "Receipt deleted successfully"},
                status=200
            )
        except Receipt.DoesNotExist:
            return Response(
                {"error": "Receipt not found"},
                status=404
            )
