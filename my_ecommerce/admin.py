from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'original_price', 'category')
    list_filter = ('category',)  # এখান থেকে ভুল 'in_stock' চিরতরে হাওয়া
    search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)
