from django.db import models
from products.models import Product
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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=10)
    qty = models.PositiveIntegerField(default=0)
    

    # from django.db import models, transaction
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# from products.models import product
# from django.conf import settings


# # Create your models here.
# class Order(models.Model):
#     STATUS_CHOICES = (
#         ("CREATED", "Created"),
#         ("SHIPPED", "Shipped"),
#         ("DELIVERED", "Delivered"),
#     )

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CREATED")
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return f"Order {self.id}"

#     def update_total(self):
#         total = sum([item.get_total() for item in self.items.all()])
#         self.total_amount = total
#         self.save(update_fields=["total_amount"])



# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
#     product = models.ForeignKey(product, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     qty = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"{self.qty} x {self.product} (@{self.price})"

#     def get_total(self):
#         return self.price * self.qty

#     def clean(self):
#         # Keep validations lightweight here; serializer-level validation is recommended for APIs
#         if self.qty < 0:
#             raise ValueError("Quantity cannot be negative")
#         # Check available stock
#         if self.product.stock_quandity < self.qty:
#             raise ValueError(f"Insufficient stock for product {self.product.sku}")


# # Signals to keep totals in sync and apply stock changes when order ships
# @receiver(post_save, sender=OrderItem)
# def update_order_total_on_item_save(sender, instance, created, **kwargs):
#     try:
#         instance.order.update_total()
#     except Exception:
#         pass


# @receiver(pre_save, sender=Order)
# def handle_order_status_change(sender, instance, **kwargs):
#     """When an Order transitions to SHIPPED, decrement product stock atomically.

#     This compares to the previous state (if any) and only acts on the transition
#     to SHIPPED. If any item lacks sufficient stock, the save will raise and
#     the transaction should be rolled back by the caller (e.g., a view).
#     """
#     if not instance.pk:
#         # New orders don't trigger stock changes here
#         return

#     # Fetch previous state
#     try:
#         previous = Order.objects.get(pk=instance.pk)
#     except Order.DoesNotExist:
#         return

#     prev_status = previous.status
#     new_status = instance.status

#     if prev_status != "SHIPPED" and new_status == "SHIPPED":
#         # Attempt to decrement stock for each item atomically
#         with transaction.atomic():
#             for item in instance.items.select_related("product").all():
#                 prod = item.product
#                 if prod.stock_quandity < item.qty:
#                     raise ValueError(f"Insufficient stock for {prod.sku}")
#                 prod.stock_quandity -= item.qty
#                 prod.save(update_fields=["stock_quandity"]) 



