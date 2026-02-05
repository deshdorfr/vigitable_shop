from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = (
        "product_image",
        "product_name",
        "price",
        "quantity",
        "subtotal",
    )
    fields = (
        "product_image",
        "product_name",
        "price",
        "quantity",
        "subtotal",
    )

    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px; object-fit:cover;" />',
                obj.product.image.url,
            )
        return obj.product#"No Image"

    product_image.short_description = "Image"

    def subtotal(self, obj):
        if obj.price and obj.quantity:
            return obj.price * obj.quantity
        else:
            return ""

    subtotal.short_description = "Sub Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__mobile", "user__name")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "price", "quantity")
    search_fields = ("product_name",)
