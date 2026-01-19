from django.urls import path
from .views import OrederCreateView,CancelOrderView
urlpatterns = [
    path('',OrederCreateView.as_view()), 
    path('<int:pk>/cancel',CancelOrderView.as_view()),
]