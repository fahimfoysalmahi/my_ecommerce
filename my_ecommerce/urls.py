from django.urls import path
from . import views  # তোর ভিউ ফাইল থেকে ফাংশনগুলো নিয়ে আসার জন্য

urlpatterns = [
    # ==========================================
    # ১. তোর ওয়েবসাইটের আগের সব রুট/লিংক (অপরিবর্তিত)
    # ==========================================
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    
    # এখানে যদি তোর আগের অন্য কোনো লিংক (যেমন ক্যালকুলেটর বা চ্যাট) থাকে, 
    # সেগুলোও এই লাইনের নিচে কমা দিয়ে বসে যাবে।
    
    # ==========================================
    # ২. নতুন যোগ হওয়া ৪টি পেমেন্ট রুট/লিংক
    # ==========================================
    path('checkout/', views.initiate_payment, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/fail/', views.payment_fail, name='payment_fail'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]
