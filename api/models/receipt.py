from django.db import models
from django.conf import settings
from api.models.base_document import BaseDocument

class Receipt(BaseDocument):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="receipts"
    )

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
    
    receipt_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Receipt - {self.merchant_name or self.id}"