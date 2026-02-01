from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
import random

@api_view(["POST"])
def place_order(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = request.data

    order = Order.objects.create(token=token, payload=payload)

    return Response({
        "success": True,
        "message": "Order placed successfully!",
        "orderId": order.id,
        "payload": payload
    })
