# store/views.py - UPDATED TO USE DATABASE
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from .models import Provider, Bundle, Router
from .serializers import ProviderSerializer, BundleSerializer, RouterSerializer

# ============ PUBLIC ENDPOINTS (Anyone can access) ============
@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    return Response({
        "status": "API is running",
        "message": "Frontend can access this endpoint",
        "authenticated": request.user.is_authenticated,
        "total_providers": Provider.objects.count(),
        "total_bundles": Bundle.objects.count(),
        "total_routers": Router.objects.count()
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_providers(request):
    """Get providers from database"""
    providers = Provider.objects.all()
    serializer = ProviderSerializer(providers, many=True)
    return Response(serializer.data)  # Returns actual database data

@api_view(['GET']) 
@permission_classes([AllowAny])
def public_bundles(request):
    """Get bundles from database"""
    bundles = Bundle.objects.all()
    serializer = BundleSerializer(bundles, many=True)
    return Response(serializer.data)  # Returns actual database data

@api_view(['GET'])
@permission_classes([AllowAny])
def public_routers(request):
    """Get routers from database"""
    routers = Router.objects.all()
    serializer = RouterSerializer(routers, many=True)
    return Response(serializer.data)  # Returns actual database data

@api_view(['POST'])
@permission_classes([AllowAny])
def public_contact(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')
    
    # You could save this to a Contact model if you create one
    return Response({
        "message": "Thank you for your message! We'll get back to you soon.",
        "received_data": {"name": name, "email": email}
    })

# ============ AUTHENTICATION ENDPOINTS ============
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

# ============ PROTECTED ENDPOINTS (Login required) ============
class ProtectedProviderViewSet(viewsets.ModelViewSet):
    """Protected providers - full data, requires login"""
    permission_classes = [IsAuthenticated]
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class ProtectedBundleViewSet(viewsets.ModelViewSet):
    """Protected bundles - full data, requires login"""
    permission_classes = [IsAuthenticated]
    queryset = Bundle.objects.all()
    serializer_class = BundleSerializer

class ProtectedRouterViewSet(viewsets.ModelViewSet):
    """Protected routers - full data, requires login"""
    permission_classes = [IsAuthenticated]
    queryset = Router.objects.all()
    serializer_class = RouterSerializer