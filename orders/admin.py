from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['food_item', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_price', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', 'payment_method']
    search_fields = ['order_number', 'user__username', 'phone']
    readonly_fields = ['order_number', 'user', 'created_at', 'updated_at']
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'total_price')}),
        ('Status', {'fields': ('status', 'payment_status', 'payment_method')}),
        ('Delivery', {'fields': ('delivery_address', 'phone', 'special_instructions', 'estimated_delivery')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    inlines = [OrderItemInline]
