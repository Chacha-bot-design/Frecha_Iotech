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
    print("🚨 ========== CREATE_ORDER START ==========")
    
    try:
        # Log the incoming request details
        print("📦 Request method:", request.method)
        print("📦 Content type:", request.content_type)
        print("📦 Raw data:", request.data)
        print("📦 User:", request.user)
        
        # Check if we have the required data
        required_fields = ['customer_name', 'email', 'phone', 'service_type', 'product_id']
        received_data = {}
        
        for field in required_fields:
            value = request.data.get(field)
            received_data[field] = value
            print(f"📦 {field}: {value} (type: {type(value)})")
        
        # Check for missing fields
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
            return Response({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print("✅ All required fields present")
        
        # Test if we can access the Order model
        print("🧪 Testing Order model access...")
        try:
            order_count = Order.objects.count()
            print(f"✅ Order model accessible. Total orders: {order_count}")
        except Exception as model_error:
            print(f"❌ Order model error: {str(model_error)}")
            raise model_error
        
        # Test the serializer
        print("🧪 Testing serializer...")
        serializer = OrderSerializer(data=request.data)
        print("📦 Serializer data:", request.data)
        
        if serializer.is_valid():
            print("✅ Serializer is valid")
            try:
                order = serializer.save()
                print(f"🎉 Order created successfully! ID: {order.id}")
                
                return Response({
                    "success": True,
                    "message": "Order created successfully!",
                    "order_id": order.id,
                    "status": order.status
                }, status=status.HTTP_201_CREATED)
                
            except Exception as save_error:
                print(f"❌ Error saving order: {str(save_error)}")
                import traceback
                print(f"🔍 Save error traceback: {traceback.format_exc()}")
                raise save_error
                
        else:
            print("❌ Serializer validation failed")
            print("🔍 Serializer errors:", serializer.errors)
            return Response({
                "success": False,
                "error": "Data validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        print(f"💥 CRITICAL ERROR in create_order: {str(e)}")
        import traceback
        error_traceback = traceback.format_exc()
        print(f"🔍 FULL TRACEBACK:\n{error_traceback}")
        
        # Return detailed error for debugging
        return Response({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "traceback": error_traceback
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        print("🚨 ========== CREATE_ORDER END ==========")

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