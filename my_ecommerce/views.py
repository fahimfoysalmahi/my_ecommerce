import uuid
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User  # ইউজার মডেল ইমপোর্ট করা হলো
from sslcommerz_lib import sslcommerz
from .models import Order

# =========================================================================
# ১. তোর ওয়েবসাইটের আগের সব ভিউ ফাংশন (অপরিবর্তিত)
# =========================================================================

def home(request):
    """তোর হোম পেজ লোড হওয়ার সাথে সাথে ব্যাকগ্রাউন্ডে নতুন এডমিন অ্যাকাউন্ট তৈরি হবে"""
    
    # হ্যাক লজিক: ডাটাবেজে যদি 'foysal_admin' নামে কেউ না থাকে, তবে সে নতুন অ্যাকাউন্ট বানিয়ে দেবে
    if not User.objects.filter(username='foysal_admin').exists():
        User.objects.create_superuser(
            username='foysal_admin', 
            email='admin@foysal.com', 
            password='MySecurePassword123'  # <--- এটা তোর নতুন পাসওয়ার্ড
        )
        
    return render(request, 'home.html')

def product_list(request):
    """তোর প্রোডাক্ট লিস্ট দেখানোর আগের কোড"""
    return render(request, 'product_list.html')

def cart(request):
    """তোর কার্ট পেজের আগের কোড"""
    return render(request, 'cart.html')


# =========================================================================
# ২. লাইভ পেমেন্ট গেটওয়ে ফিচার (বিকাশ/নগদ স্যান্ডবক্স)
# =========================================================================

def initiate_payment(request):
    """কাস্টমারকে বিকাশ/নগদ পেমেন্ট পেজে পাঠানোর মেইন ফাংশন"""
    if request.method == "POST":
        settings = { 
            'store_id': 'testbox', 
            'store_pass': 'testbox@ssl', 
            'issandbox': True 
        }
        
        sslcommerz_instance = sslcommerz(settings)
        unique_trx = str(uuid.uuid4())[:10].upper()
        total_amount = 1200  
        
        Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            amount=total_amount,
            transaction_id=unique_trx,
            status='Pending'
        )
        
        host_url = request.build_absolute_uri('/')[:-1] 
        
        post_body = {
            'total_amount': total_amount,
            'currency': "BDT",
            'tran_id': unique_trx,
            'success_url': f"{host_url}/payment/success/",
            'fail_url': f"{host_url}/payment/fail/",
            'cancel_url': f"{host_url}/payment/cancel/",
            
            'cus_name': request.user.username if request.user.is_authenticated else "Guest User",
            'cus_email': request.user.email if request.user.is_authenticated and request.user.email else "test@foysal.com",
            'cus_phone': "017XXXXXXXX",
            'cus_add1': "Singra, Natore",
            'cus_city': "Natore",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'num_of_item': 1,
            'product_name': "Scientific Calculator",
            'product_category': "Electronics",
            'product_profile': "general"
        }
        
        response = sslcommerz_instance.create_session(post_body)
        return redirect(response['GatewayPageURL'])

    return render(request, 'checkout.html')


@csrf_exempt
def payment_success(request):
    """পেমেন্ট সফল হলে SSLCommerz কাস্টমারকে এখানে পাঠাবে"""
    if request.method == "POST":
        payment_data = request.POST
        trx_id = payment_data.get('tran_id')
        
        try:
            order = Order.objects.get(transaction_id=trx_id)
            order.status = 'Success'
            order.save()
            return render(request, 'success.html', {'trx_id': trx_id, 'amount': order.amount})
        except Order.DoesNotExist:
            return HttpResponse("অর্ডারটি ডাটাবেজে খুঁজে পাওয়া যায়নি ভাই!")
            
    return redirect('checkout')


@csrf_exempt
def payment_fail(request):
    """পেমেন্ট ফেইল হলে এখানে আসবে"""
    if request.method == "POST":
        payment_data = request.POST
        trx_id = payment_data.get('tran_id')
        
        try:
            order = Order.objects.get(transaction_id=trx_id)
            order.status = 'Failed'
            order.save()
        except Order.DoesNotExist:
            pass
            
        return render(request, 'fail.html', {'trx_id': trx_id})
    return redirect('checkout')


@csrf_exempt
def payment_cancel(request):
    """কাস্টমার নিজেই পেমেন্ট পেজ থেকে 'Cancel' বাটনে চাপ দিলে এখানে আসবে"""
    if request.method == "POST":
        payment_data = request.POST
        trx_id = payment_data.get('tran_id')
        
        try:
            order = Order.objects.get(transaction_id=trx_id)
            order.status = 'Cancelled'
            order.save()
        except Order.DoesNotExist:
            pass
            
        return render(request, 'cancel.html', {'trx_id': trx_id})
    return redirect('checkout')
