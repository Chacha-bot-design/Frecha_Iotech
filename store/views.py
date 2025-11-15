# store/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Order, ServiceProvider, DataBundle, RouterProduct
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer, 
    ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer
)

# ============ ORDER VIEWSETS ============

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
    queryset = ServiceProvider.objects.filter(is_active=True)
    serializer_class = ServiceProviderSerializer
    
    @action(detail=True, methods=['get'])
    def bundles(self, request, pk=None):
        """Get bundles for a specific provider"""
        provider = self.get_object()
        bundles = DataBundle.objects.filter(provider=provider, is_active=True)
        serializer = DataBundleSerializer(bundles, many=True)
        return Response({
            'provider': ServiceProviderSerializer(provider).data,
            'bundles': serializer.data
        })

class AdminServiceProviderViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing service providers
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a service provider"""
        provider = self.get_object()
        provider.is_active = True
        provider.save()
        return Response({'status': 'provider activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a service provider"""
        provider = self.get_object()
        provider.is_active = False
        provider.save()
        return Response({'status': 'provider deactivated'})

# ============ DATA BUNDLE VIEWSETS ============

class DataBundleViewSet(viewsets.ModelViewSet):
    """
    Public ViewSet for data bundles
    """
    permission_classes = [permissions.AllowAny]
    queryset = DataBundle.objects.filter(is_active=True)
    serializer_class = DataBundleSerializer
    
    def get_queryset(self):
        queryset = DataBundle.objects.filter(is_active=True)
        provider_id = self.request.query_params.get('provider')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        return queryset

class AdminDataBundleViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing data bundles
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a data bundle"""
        bundle = self.get_object()
        bundle.is_active = True
        bundle.save()
        return Response({'status': 'bundle activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a data bundle"""
        bundle = self.get_object()
        bundle.is_active = False
        bundle.save()
        return Response({'status': 'bundle deactivated'})

# ============ ROUTER PRODUCT VIEWSETS ============

class RouterProductViewSet(viewsets.ModelViewSet):
    """
    Public ViewSet for router products
    """
    permission_classes = [permissions.AllowAny]
    queryset = RouterProduct.objects.filter(is_available=True)
    serializer_class = RouterProductSerializer

class AdminRouterProductViewSet(viewsets.ModelViewSet):
    """
    Admin ViewSet for managing router products
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = RouterProduct.objects.all()
    serializer_class = RouterProductSerializer
    
    @action(detail=True, methods=['post'])
    def make_available(self, request, pk=None):
        """Make a router product available"""
        router = self.get_object()
        router.is_available = True
        router.save()
        return Response({'status': 'router made available'})
    
    @action(detail=True, methods=['post'])
    def make_unavailable(self, request, pk=None):
        """Make a router product unavailable"""
        router = self.get_object()
        router.is_available = False
        router.save()
        return Response({'status': 'router made unavailable'})

# ============ FUNCTION-BASED VIEWS ============

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_status(request):
    """API status endpoint"""
    return Response({
        'status': 'API is running', 
        'timestamp': timezone.now(),
        'services_available': True
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_providers(request):
    """Public endpoint to get all active service providers"""
    providers = ServiceProvider.objects.filter(is_active=True)
    serializer = ServiceProviderSerializer(providers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_bundles(request):
    """Public endpoint to get all active data bundles"""
    bundles = DataBundle.objects.filter(is_active=True).select_related('provider')
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_routers(request):
    """Public endpoint to get all available router products"""
    routers = RouterProduct.objects.filter(is_available=True)
    serializer = RouterProductSerializer(routers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def all_services(request):
    """Get all services in one endpoint"""
    providers = ServiceProvider.objects.filter(is_active=True)
    bundles = DataBundle.objects.filter(is_active=True).select_related('provider')
    routers = RouterProduct.objects.filter(is_available=True)
    
    return Response({
        'providers': ServiceProviderSerializer(providers, many=True).data,
        'bundles': DataBundleSerializer(bundles, many=True).data,
        'routers': RouterProductSerializer(routers, many=True).data
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def provider_bundles(request, provider_id):
    """Get bundles for a specific provider"""
    try:
        provider = ServiceProvider.objects.get(id=provider_id, is_active=True)
        bundles = DataBundle.objects.filter(provider=provider, is_active=True)
        
        return Response({
            'provider': ServiceProviderSerializer(provider).data,
            'bundles': DataBundleSerializer(bundles, many=True).data
        })
    except ServiceProvider.DoesNotExist:
        return Response({'error': 'Provider not found'}, status=404)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_order(request):
    """Create a new order"""
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        # In a real implementation, you'd handle user association
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """Get current user info"""
    return Response({
        'username': request.user.username,
        'email': request.user.email,
        'is_staff': request.user.is_staff
    })