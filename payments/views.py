import json
import hmac
import hashlib
import uuid
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

try:
    import razorpay
except ImportError:
    razorpay = None

from orders.models import Order
from .models import Payment


@login_required(login_url='login')
def checkout(request, order_number):
    """Checkout page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
        'items': order.items.all(),
        'total': order.total_price,
    }
    return render(request, 'payment.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def process_payment(request):
    """Process payment via Razorpay"""
    try:
        order_number = request.POST.get('order_number')
        payment_method = request.POST.get('payment_method', 'razorpay')
        
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        
        if payment_method == 'cash':
            # Create payment record for cash on delivery
            transaction_id = f"COD-{uuid.uuid4().hex[:8].upper()}"
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price,
                status='pending',
                payment_method='Cash on Delivery',
                transaction_id=transaction_id
            )
            order.payment_status = 'pending'
            order.status = 'confirmed'
            order.save()
            messages.success(request, 'Order confirmed! Please pay at delivery.')
            return redirect('payment_success')
        
        # Razorpay integration
        if not razorpay:
            messages.error(request, 'Razorpay not configured. Please use Cash on Delivery.')
            return redirect('checkout', order_number=order_number)
        
        # Initialize Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': int(order.total_price * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': order.order_number,
        })
        
        # Create Payment record
        transaction_id = f"RAZ-{uuid.uuid4().hex[:8].upper()}"
        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.total_price,
            status='pending',
            razorpay_order_id=razorpay_order['id'],
            transaction_id=transaction_id
        )
        
        context = {
            'order': order,
            'payment': payment,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': int(order.total_price * 100),
        }
        return render(request, 'razorpay_checkout.html', context)
        
    except Exception as e:
        messages.error(request, f'Payment processing failed: {str(e)}')
        return redirect('view_cart')


@csrf_exempt
@require_http_methods(["POST"])
def verify_payment(request):
    """Verify Razorpay payment"""
    try:
        data = json.loads(request.body)
        
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        # Get payment record
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        
        # Verify signature
        if razorpay:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            
            try:
                client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature,
                })
            except:
                payment.status = 'failed'
                payment.save()
                payment.order.payment_status = 'failed'
                payment.order.save()
                return JsonResponse({'success': False, 'message': 'Payment verification failed'})
        
        # Update payment record
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'completed'
        payment.save()
        
        # Update order
        order = payment.order
        order.payment_status = 'completed'
        order.status = 'confirmed'
        order.save()
        
        return JsonResponse({'success': True, 'message': 'Payment verified successfully'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required(login_url='login')
def payment_success(request):
    """Payment success page"""
    orders = Order.objects.filter(user=request.user, payment_status='completed').order_by('-created_at')[:1]
    context = {
        'order': orders[0] if orders else None,
    }
    return render(request, 'payment_success.html', context)


@login_required(login_url='login')
def payment_failed(request):
    """Payment failed page"""
    return render(request, 'payment_failed.html')
