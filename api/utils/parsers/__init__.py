from .invoice_parser import parse_invoice
from .receipt_parser import parse_receipt


def parse_document(text, doc_type, ocr_confidence=None):
    if doc_type == "invoice":
        return parse_invoice(text,ocr_confidence)
    if doc_type == "receipt":
        return parse_receipt(text,ocr_confidence)
    return {}