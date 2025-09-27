from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'providers', views.ServiceProviderViewSet)
router.register(r'bundles', views.DataBundleViewSet)
router.register(r'routers', views.RouterProductViewSet)  # Fixed this line
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bundles/provider/<int:provider_id>/', views.bundles_by_provider),
]