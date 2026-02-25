from django.contrib import admin
from .models import ContactMessage, RestaurantInfo


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Contact Info', {'fields': ('name', 'email', 'phone')}),
        ('Message', {'fields': ('subject', 'message')}),
        ('Status', {'fields': ('is_read',)}),
        ('Timestamp', {'fields': ('created_at',)}),
    )


@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'description')}),
        ('Contact', {'fields': ('email', 'phone', 'address')}),
        ('Working Hours', {'fields': ('opening_time', 'closing_time')}),
        ('Razorpay Settings', {'fields': ('razorpay_key_id', 'razorpay_key_secret')}),
    )
