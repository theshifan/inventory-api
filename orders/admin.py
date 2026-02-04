from django.contrib import admin, messages
from django.db import transaction
from .models import Order, OrderItem


# ---------- ADMIN ACTIONS ----------
@ admin.action(description="please select the order to mark it as deliverd")
def delivered_order(modeladmin, request, queryset):
    with transaction.atomic():
        update= queryset.filter(
            status__in =["SHIPPED"]
        ).update(status="DELIVERED")

    if update:
        messages.success(
            request,
            f"{update} order{'s' if update != 1 else ''} marked as delivered"
        )
    else:
        messages.warning(
            request,
            "the order is not deliverd yet"
        )


@admin.action(description="Mark selected orders as shipped")
def shipped_orders(modeladmin, request, queryset):
    with transaction.atomic():
        updated = queryset.filter(
            status__in=["CREATED"]
        ).update(status="SHIPPED")

    if updated:
        messages.success(
            request,
            f"{updated} order{'s' if updated != 1 else ''} marked as shipped"
        )
    else:
        messages.warning(
            request,
            "No eligible orders to ship"
        )


@admin.action(description="Cancel selected orders (restore stock)")
def cancel_orders(modeladmin, request, queryset):
    cancelled = 0

    with transaction.atomic():
        for order in queryset.select_related().prefetch_related("items__product"):

            if order.status not in ["CREATED", "SHIPPED"]:
                continue

            for item in order.items.all():
                product = item.product
                product.stock_quandity += item.qty
                product.save(update_fields=["stock_quandity"])

            order.status = "CANCELLED"
            order.save(update_fields=["status"])
            cancelled += 1

    if cancelled>0:
        messages.success(
            request,
            f"{cancelled} order{'s' if cancelled != 1 else ''} cancelled and stock restored"
        )
    else:
        messages.warning(request, "No orders were cancelled")


# ---------- INLINE ----------

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product", "qty", "price")
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# ---------- ORDER ADMIN ----------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "status", "created_at", "total_amount")
    list_filter = ("status", "created_at")
    search_fields = ("order_id", "user__username", "user__email")
    readonly_fields = ("order_id", "user", "status", "created_at", "total_amount")
    inlines = [OrderItemInline]

    actions = [cancel_orders, shipped_orders ,delivered_order]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False