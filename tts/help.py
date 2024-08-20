# Python program to translate
# speech to text and text to speech
import wave

import pythoncom
import speech_recognition as sr
from django.conf import settings
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment
from django.core.files.storage import default_storage
from django.utils.timezone import now


def file_speach_to_text(file):
    timestamp = now().strftime('%Y%m%d%H%M%S')
    file_extension = os.path.splitext(file.name)[1]
    new_filename = f'{timestamp}{file_extension}'
    file_path = default_storage.save(new_filename, file)
    audio_file_path = default_storage.path(file_path)
    if audio_file_path.lower().endswith('.mp3'):
        wav_file_path = audio_file_path.replace('.mp3', '.wav')
        convert_mp3_to_wav(audio_file_path, wav_file_path)
        os.remove(audio_file_path)
        audio_file_path = wav_file_path

    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)  # Read the entire audio file
        try:
            text = r.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            text = "Could not request results from Google Speech Recognition service; {0}".format(e)

    os.remove(audio_file_path)
    print(text)
    return text


def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")


def speak_to_text_fr_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = r.record(source)  # Read the entire audio file
        try:
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            text = "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            text = "Could not request results from Google Speech Recognition service; {0}".format(e)
        print(text)
        return text


def text_to_speak_by_gtts(text, filename):
    language = 'en'
    tts = gTTS(text=text, lang=language, tld='us', slow=False)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    tts.save(file_path)
    return file_path


def text_to_speak_by_pyttsx3(text, filename):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    engine.save_to_file(text, file_path)
    engine.runAndWait()
    return file_path


import os


def text_to_speak_by_win32com(text, filename):
    import win32com.client
    import pythoncom

    # Initialize COM
    pythoncom.CoInitialize()

    # Create the SAPI voice and file stream objects
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    speaker.Voice = voices[0]
    file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
    # Set the file path
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    # Check if the directory exists
    if not os.path.exists(os.path.dirname(file_path)):
        raise FileNotFoundError(f"Directory does not exist: {os.path.dirname(file_path)}")
        # Configure the file stream
    file_stream.Open(file_path, 3, False)  # 3 = SSFMCreateForWrite
    # Set the output to the file stream
    speaker.AudioOutputStream = file_stream
    # Speak the text (this will save to the file)
    speaker.Speak(text)
    # Close the file stream
    file_stream.Close()
    pythoncom.CoUninitialize()
    return file_path

