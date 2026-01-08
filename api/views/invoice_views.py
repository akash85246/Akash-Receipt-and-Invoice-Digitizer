import json
from decimal import Decimal
from django.http import JsonResponse
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.invoice_serializer import InvoiceSerializer
from api.serializers.invoice_serializer import InvoiceSerializer
from api.models.invoice import Invoice
from api.models.invoice import Invoice
from api.models.items import Item


class UpdateInvoiceView(View):
    permission_classes = [IsAuthenticated]

    def post(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
        except Invoice.DoesNotExist:
            return JsonResponse({"error": "Invoice not found"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        with transaction.atomic():

            #  Update invoice fields
            allowed_fields = [
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
                "is_reviewed",
            ]

            for field in allowed_fields:
                if field in data:
                    setattr(invoice, field, data[field])

            invoice.save()

            #  Handle items
            items_payload = data.get("items", [])

            ct = ContentType.objects.get_for_model(invoice)

            existing_items = {
                item.id: item
                for item in Item.objects.filter(
                    content_type=ct,
                    object_id=invoice.id
                )
            }

            received_item_ids = set()

            for item_data in items_payload:
                item_id = item_data.get("id")
                name = item_data.get("name", "")
                quantity = Decimal(item_data.get("quantity", 1))
                price = Decimal(item_data.get("price", 0))
                total_price = price * quantity

                if item_id and item_id in existing_items:
                    #  Update item
                    item = existing_items[item_id]
                    item.name = name
                    item.quantity = quantity
                    item.price = price
                    item.total_price = total_price
                    item.save()
                else:
                    #  Create new item
                    item = Item.objects.create(
                        content_type=ct,
                        object_id=invoice.id,
                        name=name,
                        quantity=quantity,
                        price=price,
                        total_price=total_price,
                    )

                received_item_ids.add(item.id)

            #  Delete removed items
            for item_id, item in existing_items.items():
                if item_id not in received_item_ids:
                    item.delete()

        serialized_invoice = InvoiceSerializer(invoice)
        return JsonResponse(serialized_invoice.data, safe=False)


class InvoiceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=id, user=request.user)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status=200)
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"},
                status=404
            )

class DeleteInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
            invoice.delete()
            return Response(
                {"message": "Invoice deleted successfully"},
                status=200
            )
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"},
                status=404
            )