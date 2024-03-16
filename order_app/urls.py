from django.urls import path
from order_app import views

app_name = 'order_app'


urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_view, name='cart-view'),

]