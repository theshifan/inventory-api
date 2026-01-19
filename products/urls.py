from django.urls import path
from .views import ProductListCreateView,ProductDetailView,StockUpdateView

urlpatterns = [
    path('',ProductListCreateView.as_view()),
    path('<int:pk>',ProductDetailView.as_view()),
    path('update-stock/<int:pk>',StockUpdateView.as_view())
   
]