from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseRedirect

def manifest_json(request):
    return JsonResponse({
        "name": "Frecha IoTech",
        "short_name": "FrechaIoTech", 
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#000000",
    })

urlpatterns = [
    # Django admin - make sure this comes BEFORE the catch-all
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/providers/', include('store.urls')),
    path('api/bundles/', include('store.urls')),
    path('api/orders/', include('store.urls')),
    
    # Manifest route
    path('manifest.json', manifest_json),
    
    # Catch-all for React app (MUST BE LAST)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]