from django.shortcuts import render, get_object_or_4000
from django.core.management import call_command
from .models import Product

# ব্যাকএন্ডে রেন্ডার সার্ভার চালু হওয়ার সাথে সাথে ডাটাবেজ টেবিল তৈরি করার ট্রিক
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print("Migration failed:", e)

# হোমপেজের ভিউ ফাংশন
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# প্রোডাক্ট ডিটেইলস পেজের ভিউ ফাংশন
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})
