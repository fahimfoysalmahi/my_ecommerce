from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from . import views

# অটোমেটিক সুপারইউজার ট্রিক
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

# লাইভ সার্ভারে প্রোডাক্টের ছবি দেখানোর রাস্তা জুঁড়ে দেওয়া হলো
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
