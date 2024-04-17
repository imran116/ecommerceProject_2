import uuid

from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.urls import reverse

from order_app.models import Order, Cart
from payment_app.forms import BillingForm
from payment_app.models import BillingAddress
from django.contrib.auth.decorators import login_required

from sslcommerz_lib import SSLCOMMERZ
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.info(request, "Your Address Saved.")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()
    return render(request, 'payment_app/checkout.html',
                  context={'form': form, 'order_items': order_items, 'order_total': order_total,
                           'saved_address': saved_address})


@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, "Please complete shipping address.")
        return redirect('payment_app:checkout')
    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please complete profile details.")
        return redirect('login_app:profile')

    store_id = 'picka6605a4eebe0f2'
    store_pass = 'picka6605a4eebe0f2@ssl'
    payment_status_url = request.build_absolute_uri(reverse('payment_app:payment-status'))
    # print(payment_status_url)
    current_user = request.user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_items_count = order_qs[0].order_items.count()
    order_totals = order_qs[0].get_totals()
    tran_id = str(uuid.uuid4()).replace("-", "")[:13]
    settings = {'store_id': store_id, 'store_pass': store_pass, 'issandbox': True}
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = Decimal(order_totals)
    post_body['currency'] = "BDT"
    post_body['tran_id'] = tran_id
    post_body['success_url'] = payment_status_url
    post_body['fail_url'] = payment_status_url
    post_body['cancel_url'] = payment_status_url
    post_body['emi_option'] = 0
    post_body['cus_name'] = current_user.profile.full_name
    post_body['cus_email'] = current_user.email
    post_body['cus_phone'] = current_user.profile.phone
    post_body['cus_add1'] = current_user.profile.address_1
    post_body['cus_city'] = current_user.profile.city
    post_body['cus_country'] = current_user.profile.country
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = "None"
    post_body['num_of_item'] = order_items_count
    post_body['product_name'] = order_items
    post_body['product_category'] = "Mixed"
    post_body['product_profile'] = "None"
    # post_body['ship_name'] = "None"

    response = sslcommez.createSession(post_body)
    # print(response)

    return redirect(response['GatewayPageURL'])


@csrf_exempt
def complete_url_view(request):
    if request.method == 'POST' or request.method == 'post':
        payment_details = request.POST
        status = payment_details['status']

        if status == 'VALID':
            tran_id = payment_details['tran_id']
            val_id = payment_details['val_id']
            messages.info(request, "Your payment completed successfully.")
            return HttpResponseRedirect(reverse("payment_app:purchase", kwargs={'val_id': val_id, 'tran_id': tran_id}))
        if status == 'FAILED':
            messages.info(request, 'Your payment failed! Please try again. Page will be redirected after 5 seconds')

    return render(request, 'payment_app/complete.html', context={})


@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()
    cart_item = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_item:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('shop_app:home'))


@login_required
def orderList(request):
    try:
        order_list = Order.objects.filter(user=request.user, ordered=True)
    except:
        messages.info(request, "You do not have any order.")
        return redirect('shop_app:home')
    return render(request, 'payment_app/order.html', context={'order_list': order_list})
