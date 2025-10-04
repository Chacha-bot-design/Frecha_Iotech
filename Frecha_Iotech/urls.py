from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import routers
from rest_framework.decorators import api_view
from store import views

# REST Framework router
router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'bundles', views.BundleViewSet)
router.register(r'routers', views.RouterViewSet)
router.register(r'orders', views.OrderViewSet)

# API root view using REST framework
@api_view(['GET'])
def api_root(request):
    return JsonResponse({
        "message": "Frecha Iotech REST API",
        "version": "1.0",
        "documentation": "/api/",
        "endpoints": {
            "providers": "/api/providers/",
            "bundles": "/api/bundles/",
            "routers": "/api/routers/",
            "orders": "/api/orders/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # REST framework API
    path('', api_root, name='root'),
]