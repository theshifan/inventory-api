from rest_framework import serializers
from models import OrderItem,Order
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
        order = order.objects.create(user=user)

        for items in items_data:
            product = items['product']
            Qty = items['Qty']
        
            if product.stock_quandity < items:
                raise serializers.ValidationError(f"insufficeient stock for {product.name}")
            product.stock_quandity-=Qty
            product.save()
        
        
        return Order