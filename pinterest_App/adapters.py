from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken

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
    After successful Google auth, generate JWT tokens and redirect to React.
    """
    
    def get_login_redirect_url(self, request):
        print("🔥 SOCIAL ADAPTER - get_login_redirect_url called")
        print(f"   - User: {request.user}")
        print(f"   - Is authenticated: {request.user.is_authenticated}")
        
        if request.user.is_authenticated:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(request.user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Build redirect URL with tokens
            redirect_url = (
                f"{FRONTEND_URL}/auth/google/callback"
                f"?access={access_token}&refresh={refresh_token}"
                f"&user_id={request.user.id}&username={request.user.username}"
            )
            
            print(f"✅ Redirecting to React with tokens: {redirect_url[:100]}...")
            return redirect_url
        
        # Fallback if user is not authenticated
        print("⚠️ User not authenticated, redirecting to login")
        return f"{FRONTEND_URL}/login?error=auth_failed"
