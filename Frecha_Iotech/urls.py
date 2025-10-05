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

# Block function for public
def block_everything(request, *args, **kwargs):
    return JsonResponse({
        "error": "Access denied",
        "message": "This API is private and only accessible through the official frontend"
    }, status=403)

# Secure admin access with secret key
def secure_admin(request, admin_path=''):
    """Admin access protected by secret key"""
    secret_key = request.GET.get('key')
    
    # Your super secret key - no one can guess this!
    if secret_key == os.environ.get('ADMIN_SECRET_KEY', 'frecha-admin-2024-secure-key-12345'):
        # Pass the request to the actual Django admin
        return admin.site.urls[0].callback(request)
    
    # Wrong or missing key - show access denied
    return JsonResponse({
        "error": "Admin access denied",
        "message": "Invalid or missing secret key"
    }, status=403)

urlpatterns = [
    # SECURE ADMIN ACCESS (your private entry)
    path('manage/', secure_admin),  # Your secret admin URL
    
    # PROTECTED API (only your frontend can access)
    path('api/', include(router.urls)),
    
    # BLOCK EVERYTHING ELSE
    path('admin/', block_everything),  # Block normal admin URL
    path('', block_everything),  # Block root
    path('<path:unknown_path>', block_everything),  # Block everything else
]