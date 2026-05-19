from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import User
from . import views

# একটা অটোমেটিক সুপারইউজার তৈরি করার ট্রিক
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'foysal1234')
except Exception:
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]
