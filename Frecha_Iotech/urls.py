from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import routers
from store import views
import os

# Your existing API router
router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'bundles', views.BundleViewSet)
router.register(r'routers', views.RouterViewSet)
router.register(r'orders', views.OrderViewSet)

def block_everything(request, *args, **kwargs):
    return JsonResponse({
        "error": "Access denied",
        "message": "This API is private and only accessible through the official frontend"
    }, status=403)

def secure_admin(request):
    """Admin access protected by secret key - SAFE VERSION"""
    secret_key = request.GET.get('key')
    
    # SAFE: No hardcoded key - only from environment
    expected_key = os.environ.get('ADMIN_SECRET_KEY')
    
    # If no key is set in environment, block access
    if not expected_key:
        return JsonResponse({
            "error": "Admin access disabled",
            "message": "Admin secret key not configured"
        }, status=403)
    
    if secret_key == expected_key:
        return admin.site.urls[0].callback(request)
    
    return JsonResponse({
        "error": "Admin access denied",
        "message": "Invalid or missing secret key"
    }, status=403)

urlpatterns = [
    path('manage/', secure_admin),
    path('api/', include(router.urls)),
    path('admin/', block_everything),
    path('', block_everything),
    path('<path:unknown_path>', block_everything),
]