from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('food/add/', views.add_food, name='add_food'),
    path('food/edit/<int:food_id>/', views.edit_food, name='edit_food'),
    path('food/delete/<int:food_id>/', views.delete_food, name='delete_food'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('orders/<str:order_number>/update/', views.update_order_status, name='update_order_status'),
    path('reservations/', views.manage_reservations, name='manage_reservations'),
    path('analytics/', views.analytics, name='analytics'),
    path('users/', views.manage_users, name='manage_users'),
]
