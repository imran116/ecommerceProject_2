from django.urls import path
from . import views

app_name = 'payment_app'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('payment-satus/', views.complete_url_view, name='payment-status'),
    path('purchase/<val_id>/<tran_id>/', views.purchase, name='purchase'),
    path('order-list/', views.orderList, name='order-list'),

]
