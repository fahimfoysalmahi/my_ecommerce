from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'in_stock')
    list_filter = ('category', 'in_stock')
    search_fields = ('name', 'description')
