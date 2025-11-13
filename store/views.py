# store/views.py - COMPLETE VERSION
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status
from .models import ServiceProvider, DataBundle, RouterProduct, Order
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer, OrderSerializer

# ============ PUBLIC ENDPOINTS ============
@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """API status check"""
    return Response({
        "status": "API is running",
        "service": "Frecha IoTech",
        "features": ["PostgreSQL", "REST API", "Authentication"]
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_providers(request):
    """Get active service providers"""
    providers = ServiceProvider.objects.filter(is_active=True)
    serializer = ServiceProviderSerializer(providers, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
@permission_classes([AllowAny])
def public_bundles(request):
    """Get all data bundles"""
    bundles = DataBundle.objects.select_related('provider').all()
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_routers(request):
    """Get all router products"""
    routers = RouterProduct.objects.all()
    serializer = RouterProductSerializer(routers, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Create a new order"""
    try:
        print("📦 Creating order:", request.data)
        
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "success": True,
                "message": "Order created successfully!",
                "order_id": order.id,
                "status": order.status
            }, status=201)
        
        return Response({
            "success": False,
            "error": "Validation failed",
            "details": serializer.errors
        }, status=400)
        
    except Exception as e:
        print(f"❌ Order error: {e}")
        return Response({
            "success": False,
            "error": "Internal server error"
        }, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def provider_bundles(request, provider_id):
    """Get bundles for a specific provider"""
    bundles = DataBundle.objects.filter(provider_id=provider_id)
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)

# ============ AUTHENTICATION ENDPOINTS ============
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """User login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    else:
        return Response({
            "success": False,
            "message": "Invalid credentials"
        }, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """User logout endpoint"""
    logout(request)
    return Response({
        "success": True,
        "message": "Logout successful"
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current user info"""
    return Response({
        "success": True,
        "user": {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email
        }
    })

# ============ ADMIN VIEWSETS ============
class AdminServiceProviderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class AdminDataBundleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer

class AdminRouterProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RouterProduct.objects.all()
    serializer_class = RouterProductSerializer

class AdminOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer