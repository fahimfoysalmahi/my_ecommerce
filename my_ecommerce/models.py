from django.db import models

class Product(models.Model):
    # ক্যাটাগরির জন্য অপশন
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('calculators', 'Calculators'),
        ('mobiles', 'Mobiles'),
        ('others', 'Others'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # অফার দেখানোর জন্য
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    in_stock = models.BooleanField(default=True) # স্টক আছে কি না

    def __str__(self):
        return self.name
