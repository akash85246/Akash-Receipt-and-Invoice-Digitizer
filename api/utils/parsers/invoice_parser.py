import re
from datetime import datetime, timedelta
from .categorizer import auto_classify_category
from .expense_type import classify_expense_type
from .patterns import INVOICE_NO_PATTERNS, DUE_DATE_PATTERNS, UNPAID_PATTERNS, PAID_PATTERNS
from .normalizers import normalize_text
from .document_parser import base_document_data


def extract_invoice_number(text):
    text = normalize_text(text)

    for pattern in INVOICE_NO_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()

            # sanity check (length + digits)
            if len(value) >= 3 and any(c.isdigit() for c in value):
                return value

    return None


def extract_due_date(text, invoice_date=None):
    """
    Extracts invoice due date from text.
    Supports absolute dates and relative terms like 'Due in 30 days'.
    """
    text = normalize_text(text)

    for pattern in DUE_DATE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            continue

        value = match.group(1)

        # Relative date: "Due in 30 days"
        if value.isdigit() and invoice_date:
            try:
                return invoice_date + timedelta(days=int(value))
            except Exception:
                continue

        # Absolute date formats
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
                    "%Y-%m-%d", "%Y/%m/%d",
                    "%d %b %Y", "%d %B %Y"):
            try:
                return datetime.strptime(value.replace("-", "/"), fmt).date()
            except ValueError:
                pass

    return None



def extract_is_paid_with_confidence(text):
    text = normalize_text(text).lower()

    for pattern in UNPAID_PATTERNS:
        if re.search(pattern, text):
            return False, 0.9

    for pattern in PAID_PATTERNS:
        if re.search(pattern, text):
            return True, 0.9

    return None, 0.3


def parse_invoice(text,ocr_confidence=None):
    text = normalize_text(text)
    data = base_document_data(text, ocr_confidence=None)
    category = auto_classify_category(text)
    payment_mode=None

    data.update({
        "invoice_number": extract_invoice_number(text),
        "due_date": extract_due_date(text),
        "is_paid": extract_is_paid_with_confidence(text),
        "expense_type": classify_expense_type(text, category,payment_mode,ocr_confidence),

    })

    return data
