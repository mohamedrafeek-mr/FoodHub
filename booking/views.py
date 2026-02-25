from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Reservation


@require_http_methods(["GET", "POST"])
def book_table(request):
    """Book a table"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        reservation_date = request.POST.get('reservation_date')
        reservation_time = request.POST.get('reservation_time')
        number_of_guests = request.POST.get('number_of_guests')
        special_requests = request.POST.get('special_requests', '')
        
        user = request.user if request.user.is_authenticated else None
        
        reservation = Reservation.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            number_of_guests=number_of_guests,
            special_requests=special_requests
        )
        
        messages.success(request, 'Table reservation confirmed! Check your email for confirmation.')
        return redirect('home')
    
    context = {}
    return render(request, 'book_table.html', context)


@login_required(login_url='login')
def my_reservations(request):
    """View user's table reservations"""
    reservations = Reservation.objects.filter(user=request.user)
    context = {
        'reservations': reservations,
    }
    return render(request, 'my_reservations.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def cancel_reservation(request, reservation_id):
    """Cancel a reservation"""
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    
    if reservation.status not in ['pending', 'confirmed']:
        messages.error(request, 'Cannot cancel this reservation!')
        return redirect('my_reservations')
    
    reservation.status = 'cancelled'
    reservation.save()
    messages.success(request, 'Reservation cancelled successfully!')
    return redirect('my_reservations')
