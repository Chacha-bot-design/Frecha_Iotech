# store/security_middleware.py
import re
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Add security headers to every response
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response

class InputValidationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.malicious_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'(\%27)|(\')|(\-\-)|(\%23)|(#)',
        ]

    def __call__(self, request):
        # Check GET parameters
        for param, value in request.GET.items():
            if self.is_malicious(str(value)):
                return HttpResponseForbidden('Suspicious input detected')
        
        # Check POST data
        if request.method == 'POST':
            for param, value in request.POST.items():
                if self.is_malicious(str(value)):
                    return HttpResponseForbidden('Suspicious input detected')
        
        return self.get_response(request)
    
    def is_malicious(self, input_string):
        for pattern in self.malicious_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                return True
        return False