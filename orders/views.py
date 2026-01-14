from django.shortcuts import render,generics,permissions
from serializers import OrderItemSerializer
from .models import Order

# Create your views here.


class OrederCreateView(generics.ListCreateView):
    serializer_class = OrderItemSerializer
    Permission_classes = [permissions.IsAuthenicated]
   
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

    