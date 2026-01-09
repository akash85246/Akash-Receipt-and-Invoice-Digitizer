import re
from decimal import Decimal
from .normalizers import normalize_text
from .document_parser import base_document_data
from .patterns import PAYMENT_KEYWORDS, RECEIPT_NO_PATTERNS
from .categorizer import auto_classify_category
from .expense_type import classify_expense_type

def extract_payment_mode_with_confidence(text):
    text = normalize_text(text).lower()
    scores = {}

    for mode, keywords in PAYMENT_KEYWORDS.items():
        scores[mode] = sum(1 for k in keywords if k in text)

    best_mode = max(scores, key=scores.get)
    return best_mode if scores[best_mode] > 0 else None


def extract_receipt_number(text):
    text = normalize_text(text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    for pattern in RECEIPT_NO_PATTERNS:
        for line in lines:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                value = match.group(1).strip()

             
                if re.search(r"\d{3}[-\s]\d{3}[-\s]\d{4}", value):
                    continue

                return value

    return None


def parse_receipt(text, ocr_confidence=None):
    text = normalize_text(text)
    data = base_document_data(text, ocr_confidence=None)
    category = auto_classify_category(text)
    payment_mode=extract_payment_mode_with_confidence(text) or None
    data.update({
        "payment_mode": payment_mode,
        "receipt_number": extract_receipt_number(text),
        "expense_type": classify_expense_type(text, category,payment_mode,ocr_confidence),
    })

    return data
