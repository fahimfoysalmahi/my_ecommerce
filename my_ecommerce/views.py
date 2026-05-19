import uuid
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from sslcommerz_lib import sslcommerz  # এখানে সব ছোট হাতের অক্ষরে ঠিক করে দেওয়া হয়েছে
from .models import Order

# =========================================================================
# ১. তোর ওয়েবসাইটের আগের সব ভিউ ফাংশন (অপরিবর্তিত)
# =========================================================================

def home(request):
    """তোর হোম পেজের আগের কোড"""
    return render(request, 'home.html')

def product_list(request):
    """তোর প্রোডাক্ট লিস্ট দেখানোর আগের কোড"""
    return render(request, 'product_list.html')

def cart(request):
    """তোর কার্ট পেজের আগের কোড"""
    return render(request, 'cart.html')

# এখানে যদি তোর আগের অন্য কোনো ফাংশন থাকে (যেমন ক্যালকুলেটর বা চ্যাট), 
# সেগুলোও এই লাইনের নিচে যেভাবে ছিল সেভাবে রেখে দিতে পারিস।


# =========================================================================
# ২. নতুন লাইভ পেমেন্ট গেটওয়ে ফিচার (বিকাশ/নগদ স্যান্ডবক্স)
# =========================================================================

def initiate_payment(request):
    """কাস্টমারকে বিকাশ/নগদ পেমেন্ট পেজে পাঠানোর মেইন ফাংশন"""
    if request.method == "POST":
        # SSLCommerz ফ্রি স্যান্ডবক্স ক্রেডেনশিয়ালস
        settings = { 
            'store_id': 'testbox', 
            'store_pass': 'testbox@ssl', 
            'issandbox': True 
        }
        
        # এখানে 'sslcommerz' ক্লাসটি ছোট হাতের অক্ষরে কল করা হয়েছে (রেন্ডার এরর ফিক্স)
        sslcommerz_instance = sslcommerz(settings)
        
        # একটি ইউনিক ট্রানজেকশন আইডি এবং ডামি দাম (৳১২০০) তৈরি
        unique_trx = str(uuid.uuid4())[:10].upper()
        total_amount = 1200  
        
        # ডাটাবেজে অর্ডারটি সাময়িকভাবে 'Pending' হিসেবে সেভ করা
        Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            amount=total_amount,
            transaction_id=unique_trx,
            status='Pending'
        )
        
        # রেন্ডার বা লোকালহোস্টের ডাইনামিক ডোমেইন সেটআপ
        host_url = request.build_absolute_uri('/')[:-1] 
        
        # SSLCommerz-এর রিকোয়েস্ট বডি (প্রয়োজনীয় সব ডাটা)
        post_body = {
            'total_amount': total_amount,
            'currency': "BDT",
            'tran_id': unique_trx,
            'success_url': f"{host_url}/payment/success/",
            'fail_url': f"{host_url}/payment/fail/",
            'cancel_url': f"{host_url}/payment/cancel/",
            
            # কাস্টমারের ডামি ইনফরমেশন (যা গেটওয়ে পেজে দেখাবে)
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
        
        # পেমেন্ট সেশন তৈরি করা
        response = sslcommerz_instance.create_session(post_body)
        
        # কাস্টমারকে বিকাশ/নগদের অফিশিয়াল ডামি পেজে পাঠিয়ে দেওয়া
        return redirect(response['GatewayPageURL'])

    return render(request, 'checkout.html')


@csrf_exempt
def payment_success(request):
    """পেমেন্ট সফল হলে SSLCommerz কাস্টমারকে এখানে পাঠাবে"""
    if request.method == "POST":
        payment_data = request.POST
        trx_id = payment_data.get('tran_id')
        
        try:
            # ডাটাবেজ থেকে অর্ডারটি খুঁজে বের করে 'Success' করে দেওয়া
            order = Order.objects.get(transaction_id=trx_id)
            order.status = 'Success'
            order.save()
            return render(request, 'success.html', {'trx_id': trx_id, 'amount': order.amount})
        except Order.DoesNotExist:
            return HttpResponse("অর্ডারটি ডাটাবেজে খুঁজে পাওয়া যায়নি ভাই!")
            
    return redirect('checkout')


@csrf_exempt
def payment_fail(request):
    """পেমেন্ট ফেইল বা ভুল পাসওয়ার্ড/ওটিপি দিলে এখানে আসবে"""
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
