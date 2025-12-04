from django.urls import path
from .views import CartView, AddToCartView, CartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart_detail'),
    path('add/', AddToCartView.as_view(), name='cart_add'),
    path('items/<int:pk>/', CartItemView.as_view(), name='cart_item_detail'),
]
