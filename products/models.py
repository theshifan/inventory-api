from django.db import models

# Create your models here.
class product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=300,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quandity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now=True)

    def is_lowstock(self):
        return self.stock_quandity <= self.low_stock_threshold
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    