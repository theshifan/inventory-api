from rest_framework import generics
from .models import product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser,IsAuthenticated




class ProductListCreateView(generics.ListCreateAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == ['PUT','PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
