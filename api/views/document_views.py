from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from api.models.invoice import Invoice
from api.models.receipt import Receipt
from api.utils.ocr import extract_text_from_image
from api.utils.document_parser import parse_document
from api.serializers.invoice_serializer import InvoiceSerializer
from api.serializers.receipt_serializer import ReceiptSerializer



class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "pdf"]

    def post(self, request):
        files = request.FILES.getlist("files")

        if not files:
            return Response(
                {"error": "No files uploaded"},
                status=400
            )

        results = []

        for file in files:
            ext = file.name.split(".")[-1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                return Response(
                    {"error": f"Unsupported file type: {file.name}"},
                    status=400
                )

            filename = file.name.lower()

           
            if "invoice" in filename:
                document = Invoice.objects.create(
                    user=request.user,
                    image=file
                )
                doc_type = "invoice"
            else:
                document = Receipt.objects.create(
                    user=request.user,
                    image=file
                )
                doc_type = "receipt"

           
            extracted_text = ""
            try:
                extracted_text = extract_text_from_image(
                    document.image.path
                )
            except Exception as e:
                extracted_text = ""

            parsed_data = parse_document(extracted_text, doc_type)
            
            document.extracted_text = extracted_text
            document.merchant_name = parsed_data.get("merchant_name")
            document.total_amount = parsed_data.get("total_amount")
            document.date = parsed_data.get("date")
            document.category = parsed_data.get("category")

            # Receipt-specific
            if doc_type == "receipt":
                document.payment_mode = parsed_data.get("payment_mode")

            # Invoice-specific
            if doc_type == "invoice":
                document.invoice_number = parsed_data.get("invoice_number")
                document.gst_number = parsed_data.get("gst_number")

            document.save()

            results.append({
                "id": document.id,
                "type": doc_type,
                "filename": document.image.name,
                "extracted_text": extracted_text,
            })

        return Response(
            {
                "message": "Documents uploaded and processed successfully",
                "documents": results,
            },
            status=201
        )

class DocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        invoices = Invoice.objects.filter(user=request.user).order_by("-created_at")
        receipts = Receipt.objects.filter(user=request.user).order_by("-created_at")

        invoice_data = InvoiceSerializer(invoices, many=True).data
        receipt_data = ReceiptSerializer(receipts, many=True).data

        return Response(
            {
                "documents": invoice_data + receipt_data
            },
            status=200
        )
        
class DocumentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Try receipt first
        try:
            receipt = Receipt.objects.get(id=id, user=request.user)
            serializer = ReceiptSerializer(receipt)
            return Response(serializer.data, status=200)
        except Receipt.DoesNotExist:
            pass

        # Try invoice
        try:
            invoice = Invoice.objects.get(id=id, user=request.user)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status=200)
        except Invoice.DoesNotExist:
            return Response(
                {"error": "Document not found"},
                status=404
            )