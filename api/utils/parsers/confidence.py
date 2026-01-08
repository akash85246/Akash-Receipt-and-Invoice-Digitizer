def weighted_value(value, fallback=None, confidence=None, threshold=0.6):
    """
    Returns value only if confidence >= threshold,
    otherwise returns fallback.
    """

    if value is None:
        return fallback

    if confidence is None:
        return value

    return value if confidence >= threshold else fallback