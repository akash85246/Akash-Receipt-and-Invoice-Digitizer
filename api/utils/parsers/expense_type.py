import re
from .patterns import BUSINESS_KEYWORDS, PERSONAL_KEYWORDS

def classify_expense_type(
    text: str,
    category: str | None = None,
    payment_mode: str | None = None,
    confidence: float | None = None,
) -> str:
    """
    Returns: 'business' | 'personal'
    """

    text = (text or "").lower()

    business_score = 0
    personal_score = 0

    # Keyword scoring
    for kw in BUSINESS_KEYWORDS:
        if kw in text:
            business_score += 2

    for kw in PERSONAL_KEYWORDS:
        if kw in text:
            personal_score += 2

    # Category hints
    if category:
        c = category.lower()
        if c in {"travel", "electronics", "office", "software"}:
            business_score += 3
        if c in {"food", "shopping", "entertainment"}:
            personal_score += 3

    # Payment mode hint
    if payment_mode == "cash":
        personal_score += 1

    # Confidence fallback
    if confidence is not None and confidence < 0.6:
        return "personal"

    # Final decision
    if business_score > personal_score:
        return "business"

    return "personal"