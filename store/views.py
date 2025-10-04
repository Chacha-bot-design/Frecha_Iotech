from rest_framework import viewsets
from .models import Provider, Bundle, Router, Order
from .serializers import ProviderSerializer, BundleSerializer, RouterSerializer, OrderSerializer

class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class BundleViewSet(viewsets.ModelViewSet):
    queryset = Bundle.objects.all()
    serializer_class = BundleSerializer

class RouterViewSet(viewsets.ModelViewSet):
    queryset = Router.objects.all()
    serializer_class = RouterSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer