from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class ListView(APIView):
    def get(self, request, format=None):
        return Response({"ping": "pong2"})
