from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from menu.models import FoodItem, Category
from orders.models import Order, OrderItem
from booking.models import Reservation
from payments.models import Payment
from django.contrib.auth.models import User


def is_admin(user):
    """Check if user is admin"""
    return user.is_staff and user.is_superuser


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def dashboard(request):
    """Admin dashboard"""
    # Get statistics
    total_orders = Order.objects.count()
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    total_users = User.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Orders this week
    this_week = timezone.now() - timedelta(days=7)
    weekly_orders = Order.objects.filter(created_at__gte=this_week).count()
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'weekly_orders': weekly_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
@require_http_methods(["GET", "POST"])
def add_food(request):
    """Add new food item"""
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        available = request.POST.get('available') == 'on'
        image = request.FILES.get('image')
        
        category = Category.objects.get(pk=category_id)
        
        FoodItem.objects.create(
            name=name,
            category=category,
            description=description,
            price=price,
            available=available,
            image=image
        )
        
        messages.success(request, f'{name} added successfully!')
        return redirect('menu')
    
    context = {
        'categories': categories,
    }
    return render(request, 'dashboard/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
@require_http_methods(["GET", "POST"])
def edit_food(request, food_id):
    """Edit food item"""
    food_item = get_object_or_404(FoodItem, pk=food_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        food_item.name = request.POST.get('name')
        food_item.category_id = request.POST.get('category')
        food_item.description = request.POST.get('description')
        food_item.price = request.POST.get('price')
        food_item.available = request.POST.get('available') == 'on'
        
        if request.FILES.get('image'):
            food_item.image = request.FILES.get('image')
        
        food_item.save()
        messages.success(request, 'Food item updated successfully!')
        return redirect('menu')
    
    context = {
        'food_item': food_item,
        'categories': categories,
    }
    return render(request, 'dashboard/edit_food.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
@require_http_methods(["POST"])
def delete_food(request, food_id):
    """Delete food item"""
    food_item = get_object_or_404(FoodItem, pk=food_id)
    food_name = food_item.name
    food_item.delete()
    messages.success(request, f'{food_name} deleted successfully!')
    return redirect('menu')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def manage_orders(request):
    """Manage all orders"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'status': status,
    }
    return render(request, 'dashboard/manage_orders.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
@require_http_methods(["GET", "POST"])
def update_order_status(request, order_number):
    """Update order status"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated!')
        
        return redirect('manage_orders')
    
    # GET request - show form to update status
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'dashboard/update_order_status.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def manage_reservations(request):
    """Manage table reservations"""
    reservations = Reservation.objects.all().order_by('reservation_date', 'reservation_time')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        reservations = reservations.filter(status=status)
    
    context = {
        'reservations': reservations,
        'status': status,
    }
    return render(request, 'dashboard/manage_reservations.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def analytics(request):
    """View analytics and reports"""
    # Revenue analytics
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    today_revenue = Payment.objects.filter(
        status='completed',
        created_at__date=timezone.now().date()
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Order analytics
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='delivered').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    
    # Popular items
    popular_items = OrderItem.objects.values('food_item__name').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:10]
    # Convert to list and compute popularity percent for progress bars
    popular_list = list(popular_items)
    max_qty = max((item['total_quantity'] for item in popular_list), default=0)
    for item in popular_list:
        if max_qty > 0:
            # scale percentage to 100 max
            item['popularity_percent'] = min(100, round((item['total_quantity'] / max_qty) * 100))
        else:
            item['popularity_percent'] = 0

    context = {
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'popular_items': popular_list,
    }
    return render(request, 'dashboard/analytics.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def manage_users(request):
    """Manage users"""
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
    }
    return render(request, 'dashboard/manage_users.html', context)
