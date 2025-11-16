# Frecha_Iotech/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("""
    <h1>Frecha Iotech - Server Running ✅</h1>
    <p>Test these endpoints:</p>
    <ul>
        <li><a href="/api/status/">API Status</a></li>
        <li><a href="/api/providers/">Providers</a></li>
        <li><a href="/api/bundles/">Bundles</a></li>
        <li><a href="/api/routers/">Routers</a></li>
        <li><a href="/api/all-services/">All Services</a></li>
        <li><a href="/api/debug/">Debug Info</a></li>
        <li><a href="/admin/">Admin</a></li>
    </ul>
    <script>
        // Test all endpoints
        async function testEndpoints() {
            const endpoints = [
                '/api/status/',
                '/api/providers/',
                '/api/bundles/',
                '/api/routers/',
                '/api/all-services/',
                '/api/debug/'
            ];
            
            for (const endpoint of endpoints) {
                try {
                    const response = await fetch(endpoint);
                    console.log(endpoint, response.status, response.ok);
                } catch (error) {
                    console.error(endpoint, 'FAILED:', error);
                }
            }
        }
        testEndpoints();
    </script>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('', include('store.urls')),  # Include store URLs
]