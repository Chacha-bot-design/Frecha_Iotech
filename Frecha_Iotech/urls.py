from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from store import views

# Create router and register viewsets
router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'bundles', views.BundleViewSet)
router.register(r'routers', views.RouterViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]