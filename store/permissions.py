# Create store/permissions.py
from rest_framework import permissions

class FrontendOnly(permissions.BasePermission):
    """
    Only allow requests from your frontend domain
    """
    def has_permission(self, request, view):
        # Check if request comes from your frontend domain
        referer = request.META.get('HTTP_REFERER', '')
        return 'frecha-iotechi.onrender.com' in referer