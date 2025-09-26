from django.urls import path
from api.views import home_html_view, home_view, api_providers, api_bundles, api_bundles_by_provider, api_routers, api_create_order

urlpatterns = [
    path('', home_html_view),  # Serve React frontend
    path('api/', home_view),
    path('api/providers/', api_providers),
    path('api/bundles/', api_bundles),
    path('api/bundles/<int:provider_id>/', api_bundles_by_provider),
    path('api/routers/', api_routers),
    path('api/orders/', api_create_order),
]
