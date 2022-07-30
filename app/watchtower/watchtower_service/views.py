from django.shortcuts import render

# Create your views here.
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from watchtower_service.models import WebhookEvent


class ListView(APIView):
    def get(self, request, format=None):
        return Response({"ping": "pong2"})


class WebHookEventView(APIView):
    def post(self, request, format=None):
        contents = request.data
        WebhookEvent(event_json=contents).save()
        return Response({"ping", "Pong2"})