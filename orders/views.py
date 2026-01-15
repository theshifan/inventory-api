from django.shortcuts import render
from .serializers import OrderSerializer
from rest_framework import generics,permissions
from .models import Order

# Create your views here.


class OrederCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]      think about it later if you need to add permission for this user or not 
   
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     return context
    

