from rest_framework import generics, permissions
from .models import product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend




class ProductListCreateView(generics.ListCreateAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser]
        return [permissions.IsAuthenticated]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == ['PUT','PATCH','DELETE']:
            return [permissions.IsAdminUser]
        return [permissions.IsAuthenticated]
