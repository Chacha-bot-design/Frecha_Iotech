# store/views.py - UPDATED TO USE YOUR ACTUAL MODELS
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
    try:
        return Response({
            "status": "API is running",
            "database_status": "Connected",
            "total_providers": ServiceProvider.objects.count(),
            "total_bundles": DataBundle.objects.count(),
            "total_routers": RouterProduct.objects.count(),
            "total_orders": Order.objects.count(),
            "authenticated": request.user.is_authenticated
        })
    except Exception as e:
        return Response({
            "status": "API is running",
            "database_status": f"Error: {str(e)}",
            "authenticated": request.user.is_authenticated
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def public_providers(request):
    """Get active service providers"""
    try:
        providers = ServiceProvider.objects.filter(is_active=True)
        serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET']) 
@permission_classes([AllowAny])
def public_bundles(request):
    """Get all data bundles with provider information"""
    try:
        bundles = DataBundle.objects.select_related('provider').all()
        serializer = DataBundleSerializer(bundles, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_routers(request):
    """Get all router products"""
    try:
        routers = RouterProduct.objects.all()
        serializer = RouterProductSerializer(routers, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Create a new order"""
    try:
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "message": "Order created successfully!",
                "order_id": order.id,
                "status": order.status
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def provider_bundles(request, provider_id):
    """Get bundles for a specific provider"""
    try:
        bundles = DataBundle.objects.filter(provider_id=provider_id)
        serializer = DataBundleSerializer(bundles, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

# ============ PROTECTED ENDPOINTS (Admin only) ============
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