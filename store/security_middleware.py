# store/security_middleware.py
import re
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    """
    def process_response(self, request, response):
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response

class InputValidationMiddleware(MiddlewareMixin):
    """
    Validate inputs against common attack patterns
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.sql_patterns = [
            r'(\%27)|(\')|(\-\-)|(\%23)|(#)',
            r'((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))',
            r'\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))',
        ]
        self.xss_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'vbscript:',
            r'expression\s*\(',
        ]

    def __call__(self, request):
        # Skip validation for admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Validate GET parameters
        for param, value in request.GET.items():
            if self.is_malicious(str(value)):
                return HttpResponseForbidden('Suspicious input detected')
        
        # Validate POST data
        if request.method == 'POST':
            for param, value in request.POST.items():
                if self.is_malicious(str(value)):
                    return HttpResponseForbidden('Suspicious input detected')
        
        return self.get_response(request)
    
    def is_malicious(self, input_string):
        """Check if input contains malicious patterns"""
        if len(input_string) > 1000:  # Prevent very long inputs
            return True
            
        patterns = self.sql_patterns + self.xss_patterns
        for pattern in patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                return True
        return False