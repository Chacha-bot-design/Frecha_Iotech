from django.views.generic import TemplateView
from django.http import HttpResponse
import os

class ReactAppView(TemplateView):
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        # Check if the static files exist
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
        if not os.path.exists(static_dir):
            return HttpResponse("Static files not collected. Run: python manage.py collectstatic", status=500)
        
        return super().get(request, *args, **kwargs)