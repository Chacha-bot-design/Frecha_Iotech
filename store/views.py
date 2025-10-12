from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import ServiceProvider, DataBundle, RouterProduct, Order
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer, OrderSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
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

@api_view(['GET'])
def bundles_by_provider(request, provider_id):
    bundles = DataBundle.objects.filter(provider_id=provider_id)
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)