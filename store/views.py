from rest_framework import viewsets
from .models import ServiceProvider, DataBundle, RouterProduct, Order
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer, OrderSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class BundleViewSet(viewsets.ModelViewSet):
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer

class RouterViewSet(viewsets.ModelViewSet):
    queryset = RouterProduct.objects.all()
    serializer_class = RouterProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer