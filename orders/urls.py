from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_orders, name='my_orders'),
    path('create/', views.create_order, name='create_order'),
    path('<str:order_number>/', views.order_detail, name='order_detail'),
    path('<str:order_number>/cancel/', views.cancel_order, name='cancel_order'),
]
