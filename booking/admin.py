from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'reservation_date', 'reservation_time', 'number_of_guests', 'status', 'created_at']
    list_filter = ['status', 'reservation_date', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Guest Info', {'fields': ('name', 'email', 'phone', 'user')}),
        ('Reservation', {'fields': ('reservation_date', 'reservation_time', 'number_of_guests')}),
        ('Special Requests', {'fields': ('special_requests',)}),
        ('Status', {'fields': ('status',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
