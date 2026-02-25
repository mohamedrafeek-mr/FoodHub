from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'order', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['transaction_id', 'user__username', 'razorpay_payment_id', 'razorpay_order_id']
    readonly_fields = ['user', 'order', 'transaction_id', 'razorpay_payment_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Payment Info', {'fields': ('user', 'order', 'amount', 'status')}),
        ('Razorpay Details', {'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')}),
        ('Transaction', {'fields': ('transaction_id', 'payment_method')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
