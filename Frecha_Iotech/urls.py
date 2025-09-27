from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
import os

def debug_static_files(request):
    """Debug view to check static files"""
    static_info = {
        'static_root': settings.STATIC_ROOT,
        'static_root_exists': os.path.exists(settings.STATIC_ROOT),
        'debug': settings.DEBUG,
    }
    
    # Check specific files
    files_to_check = [
        'js/main.add70ce6.js',
        'css/main.21a10a42.css',
    ]
    
    for file_path in files_to_check:
        full_path = os.path.join(settings.STATIC_ROOT, file_path)
        static_info[file_path] = {
            'exists': os.path.exists(full_path),
            'path': full_path,
            'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0
        }
    
    return JsonResponse(static_info)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
]

# Serve React app
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)