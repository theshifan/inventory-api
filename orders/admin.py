from django.contrib import admin
from .models import Order, OrderItem
from .forms import OrderItemForm as OrderItemAdminForm


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'qty', 'price')
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'created_at', 'total_amount')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user__username', 'user__email')
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
            return False
