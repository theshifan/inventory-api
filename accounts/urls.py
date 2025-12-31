from django.urls import path
from . import views

urlspattern = [
    path('dashboard/', views.hello.as_view(), name='hello'),
]