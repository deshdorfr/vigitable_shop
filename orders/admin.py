from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from django.utils.safestring import mark_safe


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
    fields = readonly_fields

    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="border-radius:8px; object-fit:cover;" />',
                obj.product.image.url,
            )

        return mark_safe(
            '<div style="width:50px;height:50px;background:#eee;'
            'border-radius:8px;display:flex;align-items:center;'
            'justify-content:center;font-size:10px;color:#999;">No Image</div>'
        )

    product_image.short_description = "Image"

    def subtotal(self, obj):
        return obj.price * obj.quantity if obj.price and obj.quantity else "-"

    subtotal.short_description = "Sub Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__mobile", "user__name")

    readonly_fields = (
        "delivery_address_box",
        "total_amount",
        "created_at",
    )

    fieldsets = (
        ("📦 Delivery Address", {
            "fields": ("delivery_address_box",),
        }),
        ("🧾 Order Info", {
            "fields": ("user", "status", "total_amount", "created_at"),
        }),
    )

    inlines = [OrderItemInline]

    def delivery_address_box(self, obj):
        """
        Render delivery address as a styled box
        """
        if not obj.address:
            return "No address available"

        a = obj.address
        return format_html(
            """
            <div style="
                padding:12px;
                border:1px solid #ddd;
                border-radius:8px;
                background:#fafafa;
                max-width:400px;
            ">
                <strong>{}</strong><br>
                {}<br>
                {}<br>
                {}, {} - {}<br>
                📞 {}
            </div>
            """,
            a.full_name,
            a.house_no or "",
            a.street or "",
            a.city,
            a.state,
            a.pincode,
            a.mobile,
        )

    delivery_address_box.short_description = ""


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "price", "quantity")
    search_fields = ("product_name",)
