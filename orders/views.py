from django.shortcuts import render
from .serializers import OrderSerializer
from rest_framework import generics,permissions
from .models import Order
from django.db import transaction
from rest_framework.response import Response

# Create your views here.


class OrederCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]   # think about it later if you need to add permission for this user
   
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class CancelOrderView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:

            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.status == 'CANCELLED':
            return Response({"error": "order already cancelled"},status=400)    
        
        with transaction.atomic():
                for item in order.items.all():
                    product =  item.product
                    product.stock_quandity +=  item.qty
                    product.save()
                
                order.status = 'CANCELLED'
                order.save()

        return Response({"success": "order cancelled successfully"},status=200)
    
    


# class OrderListView(generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     return context
    

