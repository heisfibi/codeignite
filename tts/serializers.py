from rest_framework import serializers


class AudioUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 50 * 1024 * 1024:  # 50MB
            raise serializers.ValidationError("File size exceeds 50MB.")
        if not value.name.endswith('.mp3') and not value.name.endswith('.wav'):
            raise serializers.ValidationError("File format is not supported. Only MP3 or WAV files are allowed.")
        return value
