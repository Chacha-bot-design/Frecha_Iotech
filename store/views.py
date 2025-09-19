from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action  # Add 'action' here
from rest_framework.response import Response
from django.http import JsonResponse
from .models import ServiceProvider, DataBundle, RouterProduct, Order
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer, OrderSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    
    @action(detail=True, methods=['get'])
    def bundles(self, request, pk=None):
        provider = self.get_object()
        bundles = DataBundle.objects.filter(provider=provider)
        serializer = DataBundleSerializer(bundles, many=True)
        return Response(serializer.data)

class DataBundleViewSet(viewsets.ModelViewSet):
    queryset = DataBundle.objects.all()
    serializer_class = DataBundleSerializer

class RouterProductViewSet(viewsets.ModelViewSet):
    queryset = RouterProduct.objects.all()
    serializer_class = RouterProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Remove these duplicate functions since ViewSets handle them
# @api_view(['GET'])
# def provider_list(request):
#     providers = ServiceProvider.objects.all()
#     serializer = ServiceProviderSerializer(providers, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def bundle_list(request):
#     bundles = DataBundle.objects.all()
#     serializer = DataBundleSerializer(bundles, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def router_list(request):
#     routers = RouterProduct.objects.all()
#     serializer = RouterProductSerializer(routers, many=True)
#     return Response(serializer.data)

# Keep only the unique custom endpoint if needed
@api_view(['GET'])
def bundles_by_provider(request, provider_id):
    bundles = DataBundle.objects.filter(provider_id=provider_id)
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)