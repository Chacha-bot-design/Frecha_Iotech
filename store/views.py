# store/views.py - PRODUCTION SECURE VERSION
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

# ============ PUBLIC ENDPOINTS (No authentication required) ============
@api_view(['GET'])
@permission_classes([AllowAny])  # Only for public info
def api_status(request):
    return Response({
        "status": "API is running",
        "authenticated": request.user.is_authenticated,
        "user": request.user.username if request.user.is_authenticated else None
    })

@api_view(['POST'])
@permission_classes([AllowAny])  # Only for login
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
                "email": user.email,
                "is_staff": user.is_staff
            }
        })
    else:
        return Response({"message": "Invalid credentials"}, status=401)

# ============ PROTECTED ENDPOINTS (Authentication required) ============
class ProviderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # CHANGED: Requires login
    
    def list(self, request):
        return Response({
            "message": "Providers data",
            "user": request.user.username,  # Shows which user is accessing
            "data": [
                {"id": 1, "name": "Provider 1", "email": "provider1@example.com"},
                {"id": 2, "name": "Provider 2", "email": "provider2@example.com"}
            ]
        })

class BundleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # CHANGED: Requires login
    
    def list(self, request):
        return Response({
            "message": "Bundles data", 
            "user": request.user.username,
            "data": [
                {"id": 1, "name": "Bundle 1", "price": "99.99"},
                {"id": 2, "name": "Bundle 2", "price": "149.99"}
            ]
        })

class RouterViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # CHANGED: Requires login
    
    def list(self, request):
        return Response({
            "message": "Routers data",
            "user": request.user.username,
            "data": [
                {"id": 1, "name": "Router 1", "model": "Model X"},
                {"id": 2, "name": "Router 2", "model": "Model Y"}
            ]
        })

# ============ ADMIN ONLY ENDPOINTS ============
@api_view(['GET'])
@permission_classes([IsAdminUser])  # Only admin users
def admin_stats(request):
    return Response({
        "message": "Admin statistics",
        "data": {"total_users": 150, "revenue": 50000}
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
            "email": request.user.email,
            "is_staff": request.user.is_staff
        }
    })