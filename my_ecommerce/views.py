from django.shortcuts import render, get_object_or_404
from my_ecommerce.models import Product

def home(request):
    products = Product.objects.all()
    
    # সার্চ ফিল্টার
    query = request.GET.get('search')
    if query:
        products = products.filter(name__icontains=query)
        
    # ক্যাটাগরি ফিল্টার
    cat_filter = request.GET.get('category')
    if cat_filter:
        products = products.filter(category=cat_filter)
        
    return render(request, 'home.html', {
        'products': products, 
        'query': query,
        'cat_filter': cat_filter
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})
