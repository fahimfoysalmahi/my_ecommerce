from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from my_ecommerce import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # ডিটেইলস পেজের লিংক
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
