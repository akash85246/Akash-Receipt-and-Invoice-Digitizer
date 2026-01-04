from django.db import models
from api.models.base_document import BaseDocument
from api.models.user import User

class Receipt(BaseDocument):
    user = models.ForeignKey(
        User,
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

    def __str__(self):
        return f"Receipt - {self.merchant_name}"