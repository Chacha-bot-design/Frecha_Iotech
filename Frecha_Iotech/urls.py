

from django.contrib import admin
from django.urls import path, include  # ← THIS LINE IS CRITICAL
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/providers/', include('store.urls')),
    path('api/bundles/', include('store.urls')),
    path('api/orders/', include('store.urls')),
    
    # Serve React for all routes starting with 'app/'
    path('app/', TemplateView.as_view(template_name='index.html')),
    path('app/<path:route>', TemplateView.as_view(template_name='index.html')),
]