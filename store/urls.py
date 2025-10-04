from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'providers', views.ServiceProviderViewSet)
router.register(r'bundles', views.DataBundleViewSet)
router.register(r'routers', views.RouterProductViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bundles-by-provider/<int:provider_id>/', views.bundles_by_provider, name='bundles-by-provider'),
]