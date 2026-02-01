from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "phone", "total_amount", "created_at")
    search_fields = ("customer_name", "phone")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]
