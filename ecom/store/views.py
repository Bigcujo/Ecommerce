from django.shortcuts import render
from .models import Product

# Create your views here.


# home view 
def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products':products})

# about view
def about(request):
    return render(request, 'store/about.html', {})