from django.shortcuts import render, get_object_or_404
from .models import Product

# হোমপেজের ভিউ ফাংশন
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# প্রোডাক্ট ডিটেইলস পেজের ভিউ ফাংশন
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})
