from rest_framework import serializers
from models import OrderItem,Order
from django.db import transaction
from products.models import product

class OrderItemSerializer(serializers.ModelSerializer):
    class meta:
        model = OrderItem
        fields = ['Price','Qty']



class Order(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class meta:
        model = Order
        fields = ['id', 'status', 'items', 'created_at']
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        with transaction.atomic():
            order = order.objects.create(user=user , total_amount=0)
            for items in items_data:
                product = items['product']
                Qty = items['Qty']
        
                if product.stock_quandity < items:
                    raise serializers.ValidationError(f"insufficeient stock for {product.name}")
                product.stock_quandity-=Qty
                product.save()


                OrderItem.objects.create(
                    Order=Order,
                    product = product,
                    Qty =Qty,
                    price = product.price
                    )
                Total +=product.price * Qty
            Order.total_amount= Total
            Order.save()
        return order