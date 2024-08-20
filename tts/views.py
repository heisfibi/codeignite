import os

import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from tts.help import text_to_speak_by_gtts, file_speach_to_text, text_to_speak_by_pyttsx3, text_to_speak_by_win32com
from tts.serializers import AudioUploadSerializer
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


class SpeakToTextAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AudioUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            text = file_speach_to_text(file)
            return Response({"text": text, "success": True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TextToSpeakAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text', 'default_text')
        if text:
            file_path = text_to_speak_by_gtts(text, "first.mp3")
            #file_path = text_to_speak_by_win32com(text, "first.mp3")
            #file_path = text_to_speak_by_pyttsx3(text, "first.mp3")
            return Response({"file": file_path, "success": True})
        return Response({"file": text}, status=status.HTTP_400_BAD_REQUEST)

