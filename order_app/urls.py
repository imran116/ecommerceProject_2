from django.urls import path
from order_app import views

app_name = 'order_app'


urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove/<pk>/', views.remove_from_cart, name='cart-remove'),
    path('cart/', views.cart_view, name='cart-view'),

]