# store/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

# ============ PUBLIC ENDPOINTS (Anyone can access) ============
@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """Public API status - no authentication required"""
    return Response({
        "status": "API is running",
        "message": "Frontend can access this endpoint",
        "authenticated": request.user.is_authenticated
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_providers(request):
    """Public providers list - limited data"""
    return Response({
        "message": "Public providers data",
        "data": [
            {"id": 1, "name": "Provider 1", "type": "Basic"},
            {"id": 2, "name": "Provider 2", "type": "Basic"}
        ]
    })

@api_view(['GET']) 
@permission_classes([AllowAny])
def public_bundles(request):
    """Public bundles list - limited data"""
    return Response({
        "message": "Public bundles data",
        "data": [
            {"id": 1, "name": "Starter Bundle", "price": "99.99"},
            {"id": 2, "name": "Business Bundle", "price": "199.99"}
        ]
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_routers(request):
    """Public routers list - limited data"""
    return Response({
        "message": "Public routers data", 
        "data": [
            {"id": 1, "name": "Home Router", "type": "Basic"},
            {"id": 2, "name": "Office Router", "type": "Professional"}
        ]
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def public_contact(request):
    """Public contact form - no authentication required"""
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')
    
    # Process the contact form (save to database, send email, etc.)
    return Response({
        "message": "Thank you for your message! We'll get back to you soon.",
        "received_data": {"name": name, "email": email}
    })

# ============ PROTECTED ENDPOINTS (Login required) ============
@api_view(['POST'])
@permission_classes([AllowAny])  # This needs to be public for login
def user_login(request):
    """Login endpoint - public access"""
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

class ProtectedProviderViewSet(viewsets.ViewSet):
    """Protected providers - full data, requires login"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return Response({
            "message": "Protected providers data - full access",
            "user": request.user.username,
            "data": [
                {"id": 1, "name": "Provider 1", "email": "provider1@example.com", "phone": "123-456-7890", "internal_id": "P001"},
                {"id": 2, "name": "Provider 2", "email": "provider2@example.com", "phone": "123-456-7891", "internal_id": "P002"}
            ]
        })

class ProtectedBundleViewSet(viewsets.ViewSet):
    """Protected bundles - full data, requires login"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return Response({
            "message": "Protected bundles data - full access", 
            "user": request.user.username,
            "data": [
                {"id": 1, "name": "Starter Bundle", "price": "99.99", "description": "Basic package", "features": ["Feature 1", "Feature 2"]},
                {"id": 2, "name": "Business Bundle", "price": "199.99", "description": "Professional package", "features": ["All Features", "Priority Support"]}
            ]
        })

class ProtectedRouterViewSet(viewsets.ViewSet):
    """Protected routers - full data, requires login"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return Response({
            "message": "Protected routers data - full access",
            "user": request.user.username,
            "data": [
                {"id": 1, "name": "Home Router", "model": "HR-1000", "ip_address": "192.168.1.1", "configuration": "Advanced"},
                {"id": 2, "name": "Office Router", "model": "OR-2000", "ip_address": "192.168.1.2", "configuration": "Enterprise"}
            ]
        })

# ============ USER MANAGEMENT ============
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({"message": "Logout successful"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        }
    })