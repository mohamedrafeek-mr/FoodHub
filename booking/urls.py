from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_table, name='book_table'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
]
