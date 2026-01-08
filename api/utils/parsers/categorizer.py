from .patterns import CATEGORY_KEYWORDS
import re

def auto_classify_category(text):
    text = text.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(
            1 for kw in keywords if kw in text
        )

    best_category = max(scores, key=scores.get)
    return best_category if scores[best_category] > 0 else "other"