from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
def home(request):
    return JsonResponse({"status": "API running"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/referesh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('api/products/',include("products.urls")),
    path('api/order/',include("orders.urls")),
]
