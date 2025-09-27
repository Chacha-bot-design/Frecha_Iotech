from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
import os

def static_debug(request):
    """Comprehensive static files debug"""
    static_root = settings.STATIC_ROOT
    files_info = {}
    
    # Check specific files we're looking for
    target_files = [
        'static/js/main.add70ce6.js',
        'static/css/main.21a10a42.css',
        'static/js/main.js',
        'static/css/main.css',
    ]
    
    for file_path in target_files:
        full_path = os.path.join(static_root, file_path)
        files_info[file_path] = {
            'exists': os.path.exists(full_path),
            'path': full_path,
        }
        if os.path.exists(full_path):
            files_info[file_path]['size'] = os.path.getsize(full_path)
            files_info[file_path]['content_type'] = 'text/javascript' if file_path.endswith('.js') else 'text/css'
    
    # List all static files
    all_static_files = []
    if os.path.exists(static_root):
        for root, dirs, files in os.walk(static_root):
            for file in files:
                if file.endswith(('.js', '.css', '.html')):
                    rel_path = os.path.relpath(os.path.join(root, file), static_root)
                    all_static_files.append(rel_path)
    
    html_response = f"""
    <html>
    <body>
        <h1>Static Files Debug</h1>
        <p><strong>DEBUG:</strong> {settings.DEBUG}</p>
        <p><strong>STATIC_ROOT:</strong> {static_root}</p>
        <p><strong>STATIC_ROOT exists:</strong> {os.path.exists(static_root)}</p>
        
        <h2>Target Files Status:</h2>
        <ul>
    """
    
    for file_path, info in files_info.items():
        status = "✅ EXISTS" if info['exists'] else "❌ MISSING"
        html_response += f"<li><strong>{file_path}</strong>: {status}"
        if info['exists']:
            html_response += f" (Size: {info['size']} bytes)"
        html_response += "</li>"
    
    html_response += """
        </ul>
        
        <h2>All Static Files (JS, CSS, HTML):</h2>
        <ul>
    """
    
    for file_path in sorted(all_static_files)[:50]:  # Show first 50 files
        html_response += f"<li>{file_path}</li>"
    
    html_response += """
        </ul>
        
        <h2>Test Links:</h2>
        <ul>
            <li><a href="/static/js/main.add70ce6.js">/static/js/main.add70ce6.js</a></li>
            <li><a href="/static/css/main.21a10a42.css">/static/css/main.21a10a42.css</a></li>
            <li><a href="/">Home Page</a></li>
        </ul>
    </body>
    </html>
    """
    
    return HttpResponse(html_response)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path('debug-static/', static_debug),
]

# Serve React app
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# Development static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)