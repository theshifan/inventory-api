from django.contrib import admin

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'STATUS_CHOICES',
        'order_id'
        'user',
        'status',
        'created_at ',
        'total_amount'
        "items",
        )
    readonly_fields = ( 
        'STATUS_CHOICES',
        'order_id'
        'user',
        'status',
        'created_at ',
        'total_amount'
        )
    list_editable = ("items",)