from rest_framework import viewsets
from .models import ServiceProvider, DataBundle, RouterProduct, Order
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer, OrderSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()  # Remove .filter(is_active=True) temporarily
    serializer_class = ServiceProviderSerializer

class DataBundleViewSet(viewsets.ModelViewSet):
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer

class RouterProductViewSet(viewsets.ModelViewSet):
    queryset = RouterProduct.objects.all()
    serializer_class = RouterProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer