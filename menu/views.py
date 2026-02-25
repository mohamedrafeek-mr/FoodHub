from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import FoodItem, Category

@require_http_methods(["GET"])
def menu_list(request):
    """Display all food items"""
    food_items = FoodItem.objects.filter(available=True)
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        food_items = food_items.filter(category_id=category_id)
    
    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'menu.html', context)


@require_http_methods(["GET"])
def menu_by_category(request, category_id):
    """Display food items by category"""
    category = get_object_or_404(Category, pk=category_id)
    food_items = FoodItem.objects.filter(category=category, available=True)
    categories = Category.objects.all()
    
    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': category_id,
        'category_name': category.name,
    }
    return render(request, 'menu.html', context)


@require_http_methods(["GET"])
def menu_item_detail(request, item_id):
    """Display food item details"""
    food_item = get_object_or_404(FoodItem, pk=item_id)
    similar_items = FoodItem.objects.filter(
        category=food_item.category,
        available=True
    ).exclude(pk=item_id)[:4]
    
    context = {
        'food_item': food_item,
        'similar_items': similar_items,
    }
    return render(request, 'menu_detail.html', context)


@require_http_methods(["GET"])
def search_menu(request):
    """Search food items"""
    query = request.GET.get('q', '')
    food_items = FoodItem.objects.filter(available=True)
    categories = Category.objects.all()
    
    if query:
        food_items = food_items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = {
        'food_items': food_items,
        'categories': categories,
        'search_query': query,
    }
    return render(request, 'menu.html', context)


@require_http_methods(["GET"])
def search_api(request):
    """API endpoint for autocomplete search - returns JSON"""
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 8))
    
    if len(query) < 1:
        return JsonResponse({'items': []})
    
    items = FoodItem.objects.filter(available=True).filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query)
    ).values('id', 'name', 'price', 'image')[:limit]
    
    return JsonResponse({'items': list(items), 'query': query})


@require_http_methods(["GET"])
def search_page(request):
    """Dedicated search page with live autocomplete"""
    # If a query is provided, perform a search and render the menu with results
    query = request.GET.get('q', '').strip()
    # If query provided, render menu results. If not, render menu list (search.html may be removed).
    if query:
        food_items = FoodItem.objects.filter(available=True).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        food_items = FoodItem.objects.filter(available=True)

    categories = Category.objects.all()
    context = {
        'food_items': food_items,
        'categories': categories,
        'search_query': query,
    }
    return render(request, 'menu.html', context)
