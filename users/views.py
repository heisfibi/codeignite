from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer, RegisterSerializer


# Register API


class RegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": Token.objects.create(user=user).key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API
class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'success': True,
                    "token": token.key,
                    "user": UserSerializer(user).data
                })
        except User.DoesNotExist:
            user = None
        return Response({
            "error": "Invalid Credentials",
            'success': user
        }, status=status.HTTP_400_BAD_REQUEST)
