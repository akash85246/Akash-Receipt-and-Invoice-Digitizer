from django.db import models

class Items(models.Model):
    document_type = models.CharField(max_length=20)
    document_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)