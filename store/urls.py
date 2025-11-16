# store/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router
router = DefaultRouter()

# Register viewsets
router.register(r'providers', views.ServiceProviderViewSet, basename='provider')
router.register(r'bundles', views.DataBundleViewSet, basename='bundle')
router.register(r'routers', views.RouterProductViewSet, basename='router')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    # Include all router URLs under /api/
    path('api/', include(router.urls)),
    
    # Simple test endpoints
    path('api/status/', views.api_status, name='api-status'),
    path('api/all-services/', views.all_services, name='all-services'),
]