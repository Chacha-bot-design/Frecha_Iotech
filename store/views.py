# store/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Order  # Add other models as needed
from .serializers import OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer  # Add other serializers

# Your existing Order ViewSets (keep these)
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

# Add these missing ViewSets as simple placeholders
class AdminServiceProviderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    # Using Order as placeholder - replace with actual ServiceProvider when ready
    queryset = Order.objects.none()  
    serializer_class = OrderSerializer

class AdminDataBundleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    # Using Order as placeholder - replace with actual DataBundle when ready
    queryset = Order.objects.none()  
    serializer_class = OrderSerializer

# Add other missing ViewSets as needed
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

class DataBundleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)