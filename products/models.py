from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200,unique=True)
    sku = models.CharField(max_length=300,unique=True,editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quandity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_stock_at = models.DateTimeField(auto_now=True,null=True, blank=True)


    def is_lowstock(self):
        return self.stock_quandity <= self.low_stock_threshold
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.name[:3].upper()}-{uuid.uuid4().hex[:6].upper()}"

        super().save(*args, **kwargs)
    