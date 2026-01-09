import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files import File
from api.utils.pdf_utils import split_pdf_into_pages
from api.models.invoice import Invoice
from api.models.receipt import Receipt
from api.utils.ocr import extract_text_from_file
from api.utils.parsers import parse_document
from api.serializers.invoice_serializer import InvoiceSerializer
from api.serializers.receipt_serializer import ReceiptSerializer
from api.pagination import DocumentPagination
from api.models.ocr_metadata import OCRMetadata
from api.models.items import Item
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from pdf2image import convert_from_path
from  api.utils.parsers.confidence import weighted_value
from api.utils.ws import send_upload_event
from api.utils.preprocess_image  import PreprocessImage

def pdf_to_image(pdf_path: str, output_dir="media/tmp") -> str:
    pages = convert_from_path(
        pdf_path,
        dpi=300,
        first_page=1,
        last_page=1
    )

    image_name = f"{uuid.uuid4()}.png"
    image_path = os.path.join(output_dir, image_name)

    pages[0].save(image_path, "PNG")
    return image_path


class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "pdf"]

    def post(self, request):
        files = request.FILES.getlist("files")

        if not files:
            return Response({"error": "No files uploaded"}, status=400)

        os.makedirs("media/tmp", exist_ok=True)
        results = []

        for index, file in enumerate(files, start=1):
            send_upload_event(
                request.user.id,
                step="upload_started",
                message=f"Starting upload for {file.name}",
                progress=0
            )

            ext = file.name.split(".")[-1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                continue

            filename = file.name.lower()
            doc_type = "invoice" if "invoice" in filename else "receipt"

            # Save upload temporarily
            send_upload_event(
                request.user.id,
                "file_saved",
                f"Saving {file.name}",
                10
            )

            temp_upload_path = os.path.join("media/tmp", file.name)
            with open(temp_upload_path, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # PDF to Image
            if ext == "pdf":
                send_upload_event(
                    request.user.id,
                    "pdf_convert",
                    "Converting PDF to image",
                    20
                )
                image_path = pdf_to_image(temp_upload_path)
                os.remove(temp_upload_path)
            else:
                image_path = temp_upload_path

            # Save image to model
            with open(image_path, "rb") as img:
                django_file = File(img, name=os.path.basename(image_path))
                document = (
                    Invoice.objects.create(user=request.user, image=django_file)
                    if doc_type == "invoice"
                    else Receipt.objects.create(user=request.user, image=django_file)
                )

            # OCR
            send_upload_event(
                request.user.id,
                "ocr",
                "Running OCR on document",
                40
            )
            img = PreprocessImage.preprocess_for_ocr(document.image.path)

            ocr_result = extract_text_from_file(img)
            lines = ocr_result.get("lines", [])
            extracted_text = "\n".join(lines)
            ocr_conf = ocr_result.get("confidence")

            # Parsing
            send_upload_event(
                request.user.id,
                "parse",
                "Extracting structured fields",
                60
            )

            parsed_data = parse_document(
                extracted_text,
                doc_type,
                ocr_confidence=ocr_conf
            )

            # Save document fields
            document.processed_image = img
            document.extracted_text = extracted_text
            document.merchant_name = parsed_data.get("merchant_name")
            document.total_amount = weighted_value(
                parsed_data.get("total_amount"),
                fallback=None,
                confidence=ocr_conf
            )
            document.currency = parsed_data.get("currency")
            document.confidence_score = ocr_conf
            document.address = parsed_data.get("address")
            document.tax_amount = weighted_value(
                parsed_data.get("tax_amount"),
                fallback=None,
                confidence=ocr_conf
            )
            document.date = parsed_data.get("date")
            document.category = parsed_data.get("category")
            document.expense_type = parsed_data.get("expense_type")
            document.is_reviewed = False
            document.gst_number = parsed_data.get("gst_number")

            if doc_type == "receipt":
                document.receipt_number = parsed_data.get("receipt_number")
                document.payment_mode = parsed_data.get("payment_mode")

            if doc_type == "invoice":
                document.invoice_number = parsed_data.get("invoice_number")
                document.due_date = parsed_data.get("due_date")
                document.is_paid = parsed_data.get("is_paid")

            # Save items
            send_upload_event(
                request.user.id,
                "items",
                "Saving line items",
                75
            )

            items = parsed_data.get("items", [])
            content_type = ContentType.objects.get_for_model(document)

            with transaction.atomic():
                document.save()
                for item in items:
                    price = item.get("unit_price")
                    if not price:
                        continue
                    qty = item.get("quantity", 1)
                    Item.objects.create(
                        content_type=content_type,
                        object_id=document.id,
                        name=item.get("name"),
                        quantity=qty,
                        price=price,
                        total_price=price * qty
                    )

            # OCR Metadata
            send_upload_event(
                request.user.id,
                "metadata",
                "Saving OCR metadata",
                90
            )

            OCRMetadata.objects.create(
                content_type=content_type,
                object_id=document.id,
                engine_used=ocr_result.get("engine"),
                confidence_score=ocr_result.get("confidence"),
                raw_response={"lines": lines},
            )

            # Done
            send_upload_event(
                request.user.id,
                "completed",
                f"{file.name} processed successfully",
                100
            )

            results.append({
                "id": document.id,
                "type": doc_type,
                "filename": document.image.name,
                "ocr_engine": ocr_result.get("engine"),
            })

            if image_path.startswith("media/tmp"):
                os.remove(image_path)

        return Response(
            {
                "message": "Documents uploaded and processed successfully",
                "documents": results,
            },
            status=201,
        )
        
        
class DocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        doc_type = request.GET.get("type", "all")
        search = request.GET.get("search")
        category = request.GET.get("category")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        min_amount = request.GET.get("min_amount")
        max_amount = request.GET.get("max_amount")

        invoices = Invoice.objects.filter(user=user)
        receipts = Receipt.objects.filter(user=user)

        if doc_type == "invoice":
            receipts = Receipt.objects.none()
        elif doc_type == "receipt":
            invoices = Invoice.objects.none()

        if search:
            invoices = invoices.filter(
                Q(merchant_name__icontains=search)
                | Q(total_amount__icontains=search)
                | Q(date__icontains=search)
            )
            receipts = receipts.filter(
                Q(merchant_name__icontains=search)
                | Q(total_amount__icontains=search)
                | Q(date__icontains=search)
            )

        if category:
            category = category.lower()
            invoices = invoices.filter(category__iexact=category)
            receipts = receipts.filter(category__iexact=category)

        if start_date and end_date:
            invoices = invoices.filter(date__range=[start_date, end_date])
            receipts = receipts.filter(date__range=[start_date, end_date])

        if min_amount and max_amount:
            invoices = invoices.filter(
                total_amount__range=[min_amount, max_amount])
            receipts = receipts.filter(
                total_amount__range=[min_amount, max_amount])

        documents = list(invoices) + list(receipts)
        documents.sort(key=lambda x: x.created_at, reverse=True)

        paginator = DocumentPagination()
        paginated_docs = paginator.paginate_queryset(documents, request)

        serialized = []
        for doc in paginated_docs:
            if isinstance(doc, Invoice):
                serialized.append(InvoiceSerializer(doc).data)
            else:
                serialized.append(ReceiptSerializer(doc).data)

        return paginator.get_paginated_response(serialized)


class DeleteMultipleDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ids = request.data.get("ids", [])
        user = request.user

        if not ids:
            return Response(
                {"error": "No document IDs provided"},
                status=400
            )

        for doc_id in ids:
            try:
                receipt = Receipt.objects.get(id=doc_id, user=user)
                receipt.delete()
                continue
            except Receipt.DoesNotExist:
                pass

            try:
                invoice = Invoice.objects.get(id=doc_id, user=user)
                invoice.delete()
            except Invoice.DoesNotExist:
                pass

        return Response(
            {"message": "Documents deleted successfully"},
            status=200
        )