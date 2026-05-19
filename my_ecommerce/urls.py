from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# একটা সাময়িক টেস্ট ভিউ বানিয়ে নিলাম
def temporary_home(request):
    return HttpResponse("<h1>আলহামদুলিল্লাহ! ফয়সালের জ্যাঙ্গো ওয়েবসাইট সাকসেসফুলি লাইভ হয়েছে!</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', temporary_home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
