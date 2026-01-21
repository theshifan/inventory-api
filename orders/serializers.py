from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
    queryset=Product.objects.all(),
    source="product"
    )
    product_name = serializers.ReadOnlyField(source="product.name")
    product_sku = serializers.ReadOnlyField(source="product.sku")
    price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            "product_id",
            "product_name",
            "product_sku",
            "qty",
            "price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_id",
            "items",
            "total_amount",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "order_id",
            "total_amount",
            "created_at",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user

        with transaction.atomic():
            order = Order.objects.create(user=user)
            total = 0

            for item in items_data:
                product = item["product"]
                qty = item["qty"]

                if qty <= 0:
                    raise serializers.ValidationError(
                        "Quantity must be greater than zero"
                    )

                if product.stock_quandity < qty:
                    raise serializers.ValidationError(
                        f"Insufficient stock for {product.name}"
                    )

                product.stock_quandity -= qty
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    qty=qty,
                    price=product.price,
                ) 

                total += product.price * qty

            order.total_amount = total
            order.save()

        return order
