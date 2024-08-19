import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
# from fam.llm.fast_inference import TTS


class SpeakToTextAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # tts = TTS()
        # tts.synthesise(text="Hello World", spk_ref_path="assets/voice.mp3")
        return Response("")


class TextToSpeakAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return Response("")

