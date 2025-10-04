# urls.py
from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse
import os
from django.conf import settings

def serve_react_app(request):
    """Serve the React index.html file from staticfiles"""
    try:
        with open(os.path.join(settings.STATIC_ROOT, 'index.html'), 'r', encoding='utf-8') as f:
            return HttpResponse(f.read())
    except Exception as e:
        return HttpResponse(f"React app not ready: {str(e)}", status=500)

def health_check(request):
    return HttpResponse("Django backend is working!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    # Catch ALL routes and serve React
    re_path(r'^.*$', serve_react_app),
]