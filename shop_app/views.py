from django.shortcuts import render

# Improt Views
from django.views.generic import ListView, DeleteView

# Models
from shop_app.models import Product


# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'
