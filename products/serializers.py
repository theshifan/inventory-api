from rest_framework import serializers
from .models import product

class ProductSerializer(serializers.ModelSerializer):
    low_stock = serializers.SerializerMethodField()

    class Meta:
        model = product
        fields = '__all__'

    def get_low_stock(self, obj):
        return obj.is_lowstock()
