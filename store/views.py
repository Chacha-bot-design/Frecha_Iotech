from rest_framework import viewsets
from .models import ServiceProvider, DataBundle, Router, Order
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterSerializer, OrderSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class DataBundleViewSet(viewsets.ModelViewSet):
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer

class RouterViewSet(viewsets.ModelViewSet):
    queryset = Router.objects.all()
    serializer_class = RouterSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Optional: Function-based view for bundles by provider
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def bundles_by_provider(request, provider_id):
    bundles = DataBundle.objects.filter(provider_id=provider_id)
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)