from django.shortcuts import render

# Import Views
from django.views.generic import ListView, DeleteView

# Models
from shop_app.models import Product
# Mixin
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'


class ProductDetail(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop_app/product_detail.html'
