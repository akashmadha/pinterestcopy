from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# 🔧 PRODUCTION FIX: Use environment variable for frontend URL
import os
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Used for normal (username/password) login.
    Redirect directly to React home.
    """

    def get_login_redirect_url(self, request):
        return f"{FRONTEND_URL}/home"


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social account login (Google OAuth).
    Redirects to our JWT token endpoint after successful Google auth.
    """
    
    def get_login_redirect_url(self, request):
        print("🔥 SOCIAL ADAPTER - get_login_redirect_url called")
        print(f"   - User: {request.user}")
        print(f"   - Is authenticated: {request.user.is_authenticated}")
        redirect_url = "/api/accounts/google/jwt/"
        print(f"   - Redirecting to: {redirect_url}")
        return redirect_url
