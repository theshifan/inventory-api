from django.db import models
from products.models import product
from django.conf import settings
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES =(
        ('CREATED','Created'),
        ('SHIPPED','Shippped'),
        ('DELIVERED','Delivered'),
    )

    user=models.ForeignKey( settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='CREATED')
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    


class OrderItem(models.Model):
    Order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    Price= models.ForeignKey(product,on_delete=models.CASCADE)
    Qty = models.PositiveIntegerField()
