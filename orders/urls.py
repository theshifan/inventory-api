from django.urls import path
from .views import OrederCreateView
urlpatterns = [
    path('',OrederCreateView.as_view()), 
]