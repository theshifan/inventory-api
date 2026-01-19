from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser,IsAuthenticated




class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class StockUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class  = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]  

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        new_stock = int(request.data.get("stock_quandity"))

        if new_stock > product.stock_quandity:
            product.stock_updated_at = timezone.now()

        product.stock_quandity = new_stock
        product.save(update_fields=["stock_quandity", "stock_updated_at"])

        return Response(ProductSerializer(product).data)
