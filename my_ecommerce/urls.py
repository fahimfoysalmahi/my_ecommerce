from django.contrib import admin # জ্যাঙ্গোর অফিশিয়াল এডমিন মডিউল ইমপোর্ট
from django.urls import path
from . import views

urlpatterns = [
    # =========================================================================
    # ১. জ্যাঙ্গোর মেইন এডমিন প্যানেল রুট (যা ভুলবশত বাদ পড়েছিল)
    # =========================================================================
    path('admin/', admin.site.urls),
    
    # =========================================================================
    # ২. তোর ওয়েবসাইটের আগের সব রুট/লিংক (অপরিবর্তিত)
    # =========================================================================
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    
    # =========================================================================
    # ৩. লাইভ পেমেন্ট গেটওয়ের ৪টি নতুন রুট/লিংক
    # =========================================================================
    path('checkout/', views.initiate_payment, name='checkout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/fail/', views.payment_fail, name='payment_fail'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]
