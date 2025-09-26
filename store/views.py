from django.shortcuts import render  # 🔧 This is necessary
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ServiceProvider, DataBundle, RouterProduct
from .serializers import ServiceProviderSerializer, DataBundleSerializer, RouterProductSerializer, OrderSerializer
from rest_framework import viewsets
from .models import ServiceProvider
from .serializers import ServiceProviderSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
queryset = ServiceProvider.objects.all() 
serializer_class = ServiceProviderSerializer


@api_view(['GET'])
def home_view(request):
    data = {
        'message': 'Welcome to Frecha IoTech API',
        'endpoints': {
            'providers': '/api/providers/',
            'bundles': '/api/bundles/',
            'bundles_by_provider': '/api/bundles/<provider_id>/',
            'routers': '/api/routers/',
            'create_order': '/api/orders/'
        }
    }
    return Response(data)


# ✅ This serves your React frontend (index.html)
def home_html_view(request):
    return render(request, 'index.html')


@api_view(['GET'])
def api_providers(request):
    providers = ServiceProvider.objects.all()
    serializer = ServiceProviderSerializer(providers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_bundles(request):
    bundles = DataBundle.objects.all()
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_bundles_by_provider(request, provider_id):
    bundles = DataBundle.objects.filter(provider_id=provider_id)
    serializer = DataBundleSerializer(bundles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_routers(request):
    routers = RouterProduct.objects.all()
    serializer = RouterProductSerializer(routers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def api_create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
