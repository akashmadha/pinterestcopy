"""
Custom middleware to exempt API endpoints from CSRF checks.
"""
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForAPI(MiddlewareMixin):
    """
    Middleware to disable CSRF for API endpoints since we're using JWT authentication.
    """
    def process_request(self, request):
        # Exempt all /api/ endpoints from CSRF
        path = request.path
        print(f"🔍 CSRF Middleware - Checking path: {path}")
        
        if path.startswith('/api/'):
            # Set multiple flags to ensure CSRF is bypassed
            setattr(request, '_dont_enforce_csrf_checks', True)
            setattr(request, 'csrf_processing_done', True)
            print(f"✅ CSRF exempted for API endpoint: {path}")
        return None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Also exempt at the view level - this runs after process_request
        path = request.path
        if path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
            setattr(request, 'csrf_processing_done', True)
            print(f"✅ CSRF exempted at view level: {path}")
        return None

