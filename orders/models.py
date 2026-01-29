from django.db import models
from products.models import Product
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
    ("PLACED", "Placed"),
    ("CANCELLED", "Cancelled"),
    ("CREATED", "Created"),
    ("SHIPPED", "Shipped"),
    ("DELIVERED", "Delivered"),
)

    order_id = models.CharField(max_length=100,unique=True,null=True,blank=True,editable=False)
    user=models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='CREATED')
    created_at =models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.order_id or f'Order-{self.pk}'} ({self.user})"


    def save(self, *args,**kwargs):
        if not self.order_id:
            year = timezone.now().year
            last_order = Order.objects.filter(
                order_id__startswith=f"INV-{year}"
            ).order_by("-id").first()

            if last_order:
                last_number = int(last_order.order_id.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.order_id = f"INV-{year}-{str(new_number).zfill(4)}"

        super().save(*args, **kwargs)





class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:  # only on creation
            if self.product.stock_quandity < self.qty:
                raise ValueError("Insufficient stock")

            self.product.stock_quandity -= self.qty
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.qty}"
