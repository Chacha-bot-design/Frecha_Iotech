# store/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import Bundle, Provider, Router  # Adjust based on your actual models
from .serializers import BundleSerializer, ProviderSerializer, RouterSerializer  # You'll need these

# If you don't have models yet, use these simple ViewSets
class BundleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return Response({
            "message": "Bundles data",
            "data": [
                {"id": 1, "name": "Bundle 1"},
                {"id": 2, "name": "Bundle 2"}
            ]
        })

class ProviderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return Response({
            "message": "Providers data",
            "data": [
                {"id": 1, "name": "Provider 1"},
                {"id": 2, "name": "Provider 2"}
            ]
        })

class RouterViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return Response({
            "message": "Routers data",
            "data": [
                {"id": 1, "name": "Router 1"},
                {"id": 2, "name": "Router 2"}
            ]
        })

# Keep your existing function-based views for login/status
@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({
        "status": "API is running",
        "authenticated": request.user.is_authenticated,
        "user": request.user.username if request.user.is_authenticated else None
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    else:
        return Response({"message": "Invalid credentials"}, status=401)