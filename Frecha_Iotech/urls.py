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
        <li><a href="/admin/">Admin</a></li>
    </ul>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('', include('store.urls')),  # Include store URLs

     # ========== USER AUTHENTICATION ==========
    path('signup/', store_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', store_views.profile, name='profile'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'), 
         name='password_reset_complete'),

]