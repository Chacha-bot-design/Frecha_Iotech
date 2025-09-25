

from django.contrib import admin
from django.urls import path, include  # ← THIS LINE IS CRITICAL
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('api/providers/', include('store.urls')),
    path('api/bundles/', include('store.urls')),
    path('api/orders/', include('store.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
   
] + staticfiles_urlpatterns()