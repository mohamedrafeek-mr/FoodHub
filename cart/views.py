from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from decimal import Decimal
from menu.models import FoodItem
from .models import Cart, CartItem


def get_user_cart(user):
    """Get or create user's cart"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required(login_url='login')
def view_cart(request):
    """View shopping cart"""
    cart = get_user_cart(request.user)
    subtotal = cart.get_total()
    delivery_fee = Decimal('50.00')
    tax = round((subtotal + delivery_fee) * Decimal('0.05'), 2)
    grand_total = subtotal + delivery_fee + tax
    
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'tax': tax,
        'grand_total': grand_total,
        'item_count': cart.get_item_count(),
    }
    return render(request, 'cart.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def add_to_cart(request, item_id):
    """Add item to cart"""
    food_item = get_object_or_404(FoodItem, pk=item_id)
    cart = get_user_cart(request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        food_item=food_item,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{food_item.name} added to cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'cart_total': str(cart.get_total()),
        })
    
    return redirect('view_cart')


@login_required(login_url='login')
@require_http_methods(["POST"])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_user_cart(request.user)
    food_item = get_object_or_404(FoodItem, pk=item_id)
    
    CartItem.objects.filter(cart=cart, food_item=food_item).delete()
    messages.success(request, f'{food_item.name} removed from cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'cart_total': str(cart.get_total()),
        })
    
    return redirect('view_cart')


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_cart(request, item_id):
    """Update item quantity in cart"""
    cart = get_user_cart(request.user)
    food_item = get_object_or_404(FoodItem, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        CartItem.objects.filter(cart=cart, food_item=food_item).delete()
    else:
        cart_item = CartItem.objects.get(cart=cart, food_item=food_item)
        cart_item.quantity = quantity
        cart_item.save()
    
    messages.success(request, 'Cart updated!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'cart_total': str(cart.get_total()),
        })
    
    return redirect('view_cart')


@login_required(login_url='login')
@require_http_methods(["POST"])
def clear_cart(request):
    """Clear entire cart"""
    cart = get_user_cart(request.user)
    CartItem.objects.filter(cart=cart).delete()
    messages.success(request, 'Cart cleared!')
    return redirect('view_cart')
