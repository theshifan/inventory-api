from django.contrib import admin
from .models import Product

@admin.register(Product)
# Register your models here.
class PrdocutAdmin(admin.ModelAdmin):
    list_display=(
    'name',
    'sku',
    'price',
    'stock_quandity',
    'updated_stock_at',
    'low_stock_threshold',
    'is_lowstock',
    'created_at',
    )
    list_editable = ('stock_quandity',)
    readonly_fields = ('sku','created_at','updated_stock_at')
    search_fields = ('name','sku')
    list_filter = ('created_at',)
    ordering = ('name',)

    def is_lowstock(self, obj):
           if obj.is_lowstock():
                return "low stock"
           return "okay"
    is_lowstock.short_description = "Stock Status"  

    def is_low_stock(self, obj):
             return obj.stock_quandity <= obj.low_stock_threshold
    

    is_low_stock.boolean = True
    is_low_stock.short_description = "low stock"

