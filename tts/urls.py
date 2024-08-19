from django.urls import path
from .views import SpeakToTextAPI, TextToSpeakAPI

urlpatterns = [
    path('text-to-speak/', TextToSpeakAPI.as_view(), name='text-to-speak'),
    path('speak-to-text/', SpeakToTextAPI.as_view(), name='speak-to-text'),
]
