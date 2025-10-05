from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework import routers
from store import views
import os

router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'bundles', views.BundleViewSet)
router.register(r'routers', views.RouterViewSet)
router.register(r'orders', views.OrderViewSet)

def block_everything(request, *args, **kwargs):
    return JsonResponse({"error": "Access denied"}, status=403)

def admin_login_page(request):
    """Show a simple login form instead of URL key"""
    if request.method == 'POST':
        secret_key = request.POST.get('admin_key')
        expected_key = os.environ.get('ADMIN_SECRET_KEY')
        
        if secret_key == expected_key:
            # Set session and redirect to admin
            request.session['admin_authenticated'] = True
            return HttpResponseRedirect('/manage/')
        else:
            return HttpResponse('''
                <form method="post">
                    <h3>Admin Login</h3>
                    <input type="password" name="admin_key" placeholder="Enter admin key" required>
                    <button type="submit">Login</button>
                    <p style="color: red;">Invalid key</p>
                </form>
            ''')
    
    # Show login form
    return HttpResponse('''
        <form method="post">
            <h3>Admin Login</h3>
            <input type="password" name="admin_key" placeholder="Enter admin key" required>
            <button type="submit">Login</button>
        </form>
    ''')

def secure_admin(request):
    """Check session instead of URL parameter"""
    if request.session.get('admin_authenticated'):
        return admin.site.urls[0].callback(request)
    
    # Not authenticated, redirect to login
    return HttpResponseRedirect('/admin-login/')

urlpatterns = [
    path('admin-login/', admin_login_page),  # Login page
    path('manage/', secure_admin),           # Protected admin
    path('api/', include(router.urls)),
    path('admin/', block_everything),
    path('', block_everything),
    path('<path:unknown_path>', block_everything),
]