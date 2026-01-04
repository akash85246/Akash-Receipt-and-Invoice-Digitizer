import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from api.models.receipt import Receipt
from api.models.user import User

@method_decorator(csrf_exempt, name='dispatch')
class ReceiptView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        receipts = Receipt.objects.filter(owner=user)
        receipt_list = [
            {
                "id": receipt.id,
                "merchant_name": receipt.merchant_name,
                "amount": receipt.amount,
                "date": receipt.date,
                "payment_mode": receipt.payment_mode,
            }
            for receipt in receipts
        ]
        return JsonResponse({"receipts": receipt_list}, status=200)