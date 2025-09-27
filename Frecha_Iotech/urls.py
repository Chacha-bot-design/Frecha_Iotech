from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import HttpResponse

# Simple test views
def test_view(request):
    return HttpResponse("TEST: Django is working! API should be at /api/")

def api_debug(request):
    return HttpResponse("API debug endpoint - should show JSON data")

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include('store.urls')),
    path('api-debug/', api_debug),
    
    # Test route
    path('test/', test_view),
]

# IMPORTANT: Serve static files in production
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]

# Serve React app - BUT ONLY FOR NON-STATIC, NON-API ROUTES
# This regex excludes static files and API routes
urlpatterns += [
    re_path(r'^(?!static/|api/|admin/|test/).*$', TemplateView.as_view(template_name='index.html')),
]

# Development static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)