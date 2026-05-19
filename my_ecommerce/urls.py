from django.contrib import admin
from django.urls import path

# তোর ভিউ ফাইল থেকে সব ফাংশন ইমপোর্ট করা হচ্ছে
from . import views  

urlpatterns = [
    # ==========================================
    # ১. জ্যাঙ্গোর আসল এডমিন প্যানেল রুট (যা মিসিং ছিল)
    # ==========================================
    path('admin/', admin.site.urls),
    
    # ==========================================
    # ২. তোর ওয়েবসাইটের আগের সব রুট/লিংক (অপরিবর্তিত)
    # ==========================================
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    
    # ==========================================
    # ৩. লাইভ পেমেন্ট গেটওয়ের ৪টি নতুন রুট/লিংক
    # ==========================================
    path('checkout/', views.initiate_payment, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/fail/', views.payment_fail, name='payment_fail'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]
