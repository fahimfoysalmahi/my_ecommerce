from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # এটা তোর কম দাম (ডিসকাউন্ট প্রাইস)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # এটা তোর আসল বেশি দাম
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    # অটোমেটিক ডিসকাউন্ট পার্সেন্টেজ হিসেব করার ফাংশন
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            discount = ((self.original_price - self.price) / self.original_price) * 100
            return round(discount)
        return 0
