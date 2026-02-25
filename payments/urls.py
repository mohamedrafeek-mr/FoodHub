from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<str:order_number>/', views.checkout, name='checkout'),
    path('process/', views.process_payment, name='process_payment'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]
