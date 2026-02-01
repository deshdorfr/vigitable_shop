from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "product_name", "price", "quantity"]


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user", "address", "total_amount", "status", "created_at", "items"]
