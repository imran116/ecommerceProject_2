from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from order_app.models import Order
from payment_app.forms import BillingForm
from payment_app.models import BillingAddress
from django.contrib.auth.decorators import login_required


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
                  context={'form': form, 'order_items': order_items, 'order_total': order_total})
