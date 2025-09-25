
#############
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # API routes
    path('api/providers/', include('store.urls')),
    path('api/bundles/', include('store.urls')),
    path('api/orders/', include('store.urls')),
    
    # Serve React for all other routes
    path('', TemplateView.as_view(template_name='index.html')),
    path('<path:route>', TemplateView.as_view(template_name='index.html')),
]