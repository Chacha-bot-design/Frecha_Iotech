
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('store.urls')),  # This includes all URLs from store app
    path('admin/', admin.site.urls),
]