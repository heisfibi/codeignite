import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def text_to_speech(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')

        # Replace with your Meta Free Text-to-Speech API endpoint and key
        api_url = "https://api.meta.com/v1/tts"
        api_key = "YOUR_API_KEY"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "text": text,
            "voice": "default",  # Specify the voice if needed
            "language": "en-US"  # Specify the language if needed
        }

        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Failed to generate speech"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
