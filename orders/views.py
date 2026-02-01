from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal

from accounts.models import Address
from products.models import Product
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def orders_view(request):
    # ✅ GET: List my orders
    if request.method == "GET":
        orders = Order.objects.filter(user=request.user).order_by("-id")
        serializer = OrderSerializer(orders, many=True)
        return Response({"success": True, "data": serializer.data})

    # ✅ POST: Place new order
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    address_id = serializer.validated_data["address_id"]
    items_data = serializer.validated_data["items"]

    address = Address.objects.filter(id=address_id, user=request.user).first()
    if not address:
        return Response({"success": False, "message": "Invalid address"}, status=400)

    order = Order.objects.create(user=request.user, address=address)

    total = Decimal("0.00")

    for item in items_data:
        product = item.get("product")
        quantity = item["quantity"]

        if product:
            product_obj = Product.objects.filter(id=product.id).first()
            if not product_obj:
                continue
            price = Decimal(str(product_obj.price))
            product_name = product_obj.name
        else:
            price = Decimal(str(item["price"]))
            product_name = item["product_name"]

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product_name,
            price=price,
            quantity=quantity,
        )

        total += price * quantity

    order.total_amount = total
    order.save()

    return Response({
        "success": True,
        "message": "Order placed successfully!",
        "order": OrderSerializer(order).data
    })
