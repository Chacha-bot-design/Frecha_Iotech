# store/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Order, ServiceProvider  # Make sure ServiceProvider is imported
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer, ServiceProviderSerializer  # Make sure ServiceProviderSerializer is imported

# ============ EXISTING ORDER VIEWSETS ============

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            if self.request.user.is_staff:
                return OrderUpdateSerializer
            return OrderSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def status_counts(self, request):
        if request.user.is_staff:
            counts = {
                'total': Order.objects.count(),
                'pending': Order.objects.filter(status='pending').count(),
                'confirmed': Order.objects.filter(status='confirmed').count(),
                'processing': Order.objects.filter(status='processing').count(),
                'shipped': Order.objects.filter(status='shipped').count(),
                'delivered': Order.objects.filter(status='delivered').count(),
            }
        else:
            counts = {
                'total': Order.objects.filter(user=request.user).count(),
                'pending': Order.objects.filter(user=request.user, status='pending').count(),
                'confirmed': Order.objects.filter(user=request.user, status='confirmed').count(),
                'processing': Order.objects.filter(user=request.user, status='processing').count(),
                'shipped': Order.objects.filter(user=request.user, status='shipped').count(),
                'delivered': Order.objects.filter(user=request.user, status='delivered').count(),
            }
        return Response(counts)

class AdminOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer
    
    @action(detail=True, methods=['post'])
    def mark_processing(self, request, pk=None):
        order = self.get_object()
        order.status = 'processing'
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_shipped(self, request, pk=None):
        order = self.get_object()
        order.status = 'shipped'
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_delivered(self, request, pk=None):
        order = self.get_object()
        order.mark_completed()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

# ============ SERVICE PROVIDER VIEWSETS ============

class ServiceProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for service providers (public access)
    """
    permission_classes = [permissions.AllowAny]
    queryset = ServiceProvider.objects.all() if hasattr(ServiceProvider, 'objects') else ServiceProvider.objects.none()
    serializer_class = ServiceProviderSerializer
    
    def get_queryset(self):
        try:
            return ServiceProvider.objects.all()
        except:
            return ServiceProvider.objects.none()
    
    @action(detail=True, methods=['get'])
    def bundles(self, request, pk=None):
        """Get bundles for a specific provider"""
        provider = self.get_object()
        # You can add bundle logic here when you create Bundle model
        return Response({
            'provider': provider.name if hasattr(provider, 'name') else f"Provider {pk}",
            'bundles': []
        })

class AdminServiceProviderViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing service providers
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = ServiceProvider.objects.all() if hasattr(ServiceProvider, 'objects') else ServiceProvider.objects.none()
    serializer_class = ServiceProviderSerializer
    
    def get_queryset(self):
        try:
            return ServiceProvider.objects.all()
        except:
            return ServiceProvider.objects.none()
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a service provider"""
        provider = self.get_object()
        if hasattr(provider, 'is_active'):
            provider.is_active = True
            provider.save()
        return Response({'status': 'provider activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a service provider"""
        provider = self.get_object()
        if hasattr(provider, 'is_active'):
            provider.is_active = False
            provider.save()
        return Response({'status': 'provider deactivated'})

# ============ OTHER MISSING VIEWSETS ============

class AdminDataBundleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.none()  
    serializer_class = OrderSerializer

class AdminRouterProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

class DataBundleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

class RouterProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

# ============ FUNCTION-BASED VIEWS ============

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_status(request):
    return Response({'status': 'API is running', 'timestamp': timezone.now()})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_providers(request):
    """Public endpoint to get all service providers"""
    try:
        providers = ServiceProvider.objects.all()
        serializer = ServiceProviderSerializer(providers, many=True)
        return Response(serializer.data)
    except:
        return Response([])

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_bundles(request):
    return Response([])

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_routers(request):
    return Response([])

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def provider_bundles(request, provider_id):
    """Get bundles for a specific provider"""
    try:
        provider = ServiceProvider.objects.get(id=provider_id)
        # Return empty bundles for now - you can add actual bundles later
        return Response({
            'provider': ServiceProviderSerializer(provider).data,
            'bundles': []
        })
    except ServiceProvider.DoesNotExist:
        return Response({'error': 'Provider not found'}, status=404)
    except:
        return Response({'bundles': []})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    return Response({'error': 'Authentication not implemented yet'}, status=501)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    return Response({'message': 'Logged out successfully'})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    if request.user.is_authenticated:
        return Response({
            'username': request.user.username,
            'email': request.user.email,
            'is_staff': request.user.is_staff
        })
    return Response({'error': 'Not authenticated'}, status=401)