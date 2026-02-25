from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu'),
    path('category/<int:category_id>/', views.menu_by_category, name='menu_category'),
    path('item/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('search/', views.search_page, name='search_page'),
    path('api/search/', views.search_api, name='search_api'),
]
