# api/models/receipt.py
from django.db import models
from api.models.base_document import BaseDocument

class Receipt(BaseDocument):
    PAYMENT_MODES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("upi", "UPI"),
        ("wallet", "Wallet"),
    ]

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODES,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Receipt - {self.merchant_name or self.id}"