from rest_framework import serializers
from .models import OrderItem,Order
from django.db import transaction
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product','qty']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'total_amount', 'created_at']
        read_only_fields = ['id','total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(user=user , total_amount=0)
            total = 0

            for items in items_data:
                product = Product.objects.select_for_update().get(id=items['product'].id)
                qty = items['qty']
                
                if qty <= 0:
                    raise serializers.ValidationError("Quantity must be greater than zero")
                
                if product.stock_quandity < qty:
                    raise serializers.ValidationError(f"insufficeient stock for {product.name}")
                
                product.stock_quandity-=qty
                product.save()




                OrderItem.objects.create(
                    order=order,
                    product = product,
                    qty =qty,
                    price = product.price
                    )
                total +=product.price * qty
            order.total_amount= total
            order.save()
        return order