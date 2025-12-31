from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class hello(IsAuthenticated):
    permission_classes = (IsAuthenticated, )

    def get(self,request):
        content ={'message':'hello'}
        return Response(content)

# Create your views here.
