from rest_framework import viewsets, permissions
from .models import ServiceProvider, DataBundle, RouterProduct, Order
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer, OrderSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add this line

class BundleViewSet(viewsets.ModelViewSet):
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add this line

class RouterViewSet(viewsets.ModelViewSet):
    queryset = RouterProduct.objects.all()
    serializer_class = RouterProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add this line

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add this line