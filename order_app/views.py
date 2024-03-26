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


@login_required()
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'order_app/cart.html', context={'carts': carts, 'orders': order})
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect('shop_app:home')


@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was remove form your cart.")
            return redirect("order_app:cart-view")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect('shop_app:home')
