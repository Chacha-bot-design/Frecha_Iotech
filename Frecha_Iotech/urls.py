from django.contrib import admin
from django.urls import path, include, re_path  # ← Add re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
from django.http import JsonResponse  # ← ADD THIS MISSING IMPORT

class ManifestView(View):
    def get(self, request):
        manifest_data = {
            "name": "Frecha IoTech",
            "short_name": "FrechaIoTech",
            "description": "Frecha IoTech Application",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#000000",
            "icons": [
                {
                    "src": "/static/favicon.ico",
                    "sizes": "64x64", 
                    "type": "image/x-icon"
                }
            ]
        }
        return JsonResponse(manifest_data)  # ← Now this will work!


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/providers/', include('store.urls')),
    path('api/bundles/', include('store.urls')),
    path('api/orders/', include('store.urls')),

    # Manifest route
    path('manifest.json', ManifestView.as_view(), name='manifest'),
    
    # Serve React app - use re_path for catch-all
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# Add static files serving (only in development)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)