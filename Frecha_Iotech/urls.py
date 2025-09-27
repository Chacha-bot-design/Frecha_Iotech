from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.apps import apps

# Add this debug function
def api_debug(request):
    """Debug API configuration"""
    debug_info = {
        'installed_apps': list(apps.app_configs.keys()),
        'api_status': 'Debug endpoint working'
    }
    
    # Check if store app is installed and models exist
    try:
        from store.models import ServiceProvider, DataBundle, RouterProduct
        debug_info['store_models'] = {
            'ServiceProvider': ServiceProvider.objects.count(),
            'DataBundle': DataBundle.objects.count(), 
            'RouterProduct': RouterProduct.objects.count()
        }
    except Exception as e:
        debug_info['store_models_error'] = str(e)
    
    return JsonResponse(debug_info)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),  # This includes your API routes
    path('api-debug/', api_debug),  # ← ADD THIS LINE HERE
]

# Serve React app for all other routes
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]