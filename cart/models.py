from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem

class Cart(models.Model):
    """Shopping cart for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        """Calculate total cart value"""
        return sum(item.get_total() for item in self.items.all())
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """Individual items in cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_total(self):
        """Calculate total for this cart item"""
        return self.food_item.price * self.quantity
    
    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"
