from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from Base_app.models import ContactMessage

@require_http_methods(["GET", "POST"])
def home(request):
    """Homepage view"""
    from menu.models import FoodItem
    featured_items = FoodItem.objects.filter(available=True)[:6]
    context = {
        'featured_items': featured_items,
    }
    return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')


@require_http_methods(["GET", "POST"])
def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Create cart for user if it doesn't exist
            from cart.models import Cart
            Cart.objects.get_or_create(user=user)
            messages.success(request, f'Welcome back, {username}!')
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'login.html')


@login_required(login_url='login')
def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')


@login_required(login_url='login')
def profile(request):
    """User profile page"""
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)


@require_http_methods(["GET"])
def about(request):
    """About page"""
    return render(request, 'about.html')


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')
