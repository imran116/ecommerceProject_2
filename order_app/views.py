from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from order_app.models import Cart, Order
from shop_app.models import Product
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required()
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_obj = Order.objects.filter(user=request.user, ordered=False)
    if order_obj.exists():
        order = order_obj[0]
        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop_app:home")
        else:
            order.order_items.add(order_item[0])
            messages.info(request, "This item was added to your cart")
            return redirect("shop_app:home")
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        messages.info(request, "This item was added to your cart.")
        return redirect("shop_app:home")