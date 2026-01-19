from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "sku",
            "name",
            "price",
            "stock_quandity",
            "stock_updated_at",
            "low_stock_threshold",
            "is_lowstock",
            "created_at"
        ]
        read_only_fields = ["id", "sku", "stock_updated_at", "created_at"]


    def get_low_stock(self, obj):
        return obj.is_lowstock()
    

class StockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'stock_quandity']

    def validate_stock(self, value):
        if value <0:
            raise serializers.ValidationError("Stock quantity cannot be negative")
        return value