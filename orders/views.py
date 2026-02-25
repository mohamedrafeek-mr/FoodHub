from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import uuid
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from menu.models import FoodItem


def generate_order_number():
    """Generate unique order number"""
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"


@login_required(login_url='login')
def my_orders(request):
    """View user's orders"""
    user_orders = Order.objects.filter(user=request.user)
    context = {
        'orders': user_orders,
    }
    return render(request, 'my_orders.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def create_order(request):
    """Create order from cart"""
    cart = Cart.objects.get(user=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        phone = request.POST.get('phone')
        special_instructions = request.POST.get('special_instructions', '')
        payment_method = request.POST.get('payment_method', 'razorpay')
        
        # Create order
        total_price = cart.get_total()
        order = Order.objects.create(
            user=request.user,
            order_number=generate_order_number(),
            total_price=total_price,
            delivery_address=delivery_address,
            phone=phone,
            special_instructions=special_instructions,
            payment_method=payment_method,
            estimated_delivery=timezone.now() + timedelta(minutes=30)
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food_item=cart_item.food_item,
                quantity=cart_item.quantity,
                price=cart_item.food_item.price
            )
        
        # Clear cart
        CartItem.objects.filter(cart=cart).delete()
        
        messages.success(request, 'Order created successfully!')
        return redirect('checkout', order_number=order.order_number)
    
    subtotal = cart.get_total()
    delivery_fee = Decimal('50.00')
    tax = round((subtotal + delivery_fee) * Decimal('0.05'), 2)
    grand_total = subtotal + delivery_fee + tax
    
    context = {
        'cart': cart,
        'total': subtotal,
        'delivery_fee': delivery_fee,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def order_detail(request, order_number):
    """View order details"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
        'items': order.items.all(),
    }
    return render(request, 'order_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def cancel_order(request, order_number):
    """Cancel order"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.status not in ['pending', 'confirmed']:
        messages.error(request, 'Cannot cancel this order!')
        return redirect('order_detail', order_number=order_number)
    
    order.status = 'cancelled'
    order.save()
    messages.success(request, 'Order cancelled successfully!')
    return redirect('order_detail', order_number=order_number)
