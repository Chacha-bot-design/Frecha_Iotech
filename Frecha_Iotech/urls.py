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
    """Show a secure login form"""
    if request.method == 'POST':
        secret_key = request.POST.get('admin_key')
        expected_key = os.environ.get('ADMIN_SECRET_KEY', 'Imthewinner01-2024')
        
        print(f"DEBUG: Login attempt with key: {secret_key}")
        
        if secret_key == expected_key:
            # Set session and redirect to admin
            request.session['admin_authenticated'] = True
            print("DEBUG: Login successful, redirecting to admin")
            return HttpResponseRedirect('/manage/')
        else:
            print("DEBUG: Login failed - invalid key")
            return HttpResponse('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Admin Login - Frecha Iotech</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }
                        .login-form { background: #f5f5f5; padding: 30px; border-radius: 8px; }
                        input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
                        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
                        .error { color: red; margin-top: 10px; }
                    </style>
                </head>
                <body>
                    <div class="login-form">
                        <h3>🔒 Admin Login</h3>
                        <form method="post">
                            <input type="password" name="admin_key" placeholder="Enter admin key" 
                                   autocomplete="new-password" required>
                            <button type="submit">Login</button>
                            <div class="error">Invalid admin key</div>
                        </form>
                    </div>
                </body>
                </html>
            ''')
    
    # Show login form
    return HttpResponse('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Login - Frecha Iotech</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; max-width: 400px; margin: 100px auto; padding: 20px; }
                .login-form { background: #f5f5f5; padding: 30px; border-radius: 8px; }
                input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
                button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="login-form">
                <h3>🔒 Admin Login</h3>
                <form method="post">
                    <input type="password" name="admin_key" placeholder="Enter admin key" 
                           autocomplete="new-password" required>
                    <button type="submit">Login</button>
                </form>
            </div>
        </body>
        </html>
    ''')

def secure_admin(request):
    """Check session with proper error handling"""
    if request.session.get('admin_authenticated'):
        try:
            print("DEBUG: Session authenticated, loading admin...")
            return admin.site.urls[0].callback(request)
        except Exception as e:
            print(f"DEBUG: Admin loading error: {str(e)}")
            return HttpResponse(f'''
                <html>
                <body>
                    <h3>Admin Error</h3>
                    <p>Django admin is not accessible: {str(e)}</p>
                    <a href="/admin-login/">Try Again</a>
                </body>
                </html>
            ''')
    
    # Not authenticated
    return HttpResponse('''
        <html>
        <body>
            <h3>Access Denied</h3>
            <p>Please <a href="/admin-login/">login</a> to access the admin panel.</p>
        </body>
        </html>
    ''', status=403)

urlpatterns = [
    path('admin-login/', admin_login_page),  # Professional login page
    path('manage/', secure_admin),           # Protected admin
    path('api/', include(router.urls)),
    path('admin/', block_everything),
    path('', block_everything),
    path('<path:unknown_path>', block_everything),
]