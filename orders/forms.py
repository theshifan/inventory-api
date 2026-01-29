from django import forms
from .models import OrderItem

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"

        def clean_qty(self):
            cleaned_data = super().clean()
            product = cleaned_data.get("product")
            qty = cleaned_data.get("qty")

            if product and qty:
                if qty > product.stock_quandity:
                    raise forms.ValidationError(f"Insufficient stock. Available: {product.stock_quandity}")
            
            return cleaned_data