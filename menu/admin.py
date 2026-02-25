from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created_at']
    list_filter = ['category', 'available', 'created_at']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'category', 'description')}),
        ('Pricing & Availability', {'fields': ('price', 'available')}),
        ('Media', {'fields': ('image',)}),
    )
