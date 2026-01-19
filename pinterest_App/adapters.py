# ========================================
# 📱 CUSTOM ADAPTERS FOR GOOGLE OAUTH
# ========================================
#
# Simple Explanation:
# These adapters tell Django where to send users after they log in.
# Think of them as "traffic directors" for login redirects.
#
# Why do we need custom adapters?
# - Default Django behavior: Redirect to /accounts/profile/
# - Our app needs: Redirect to React with JWT tokens
#
# Two types of login:
# 1. Normal login (username/password) → CustomAccountAdapter
# 2. Google login (OAuth) → CustomSocialAccountAdapter
#

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken

# Get the frontend URL from environment variable
# Development: http://localhost:3000
# Production: https://your-app.vercel.app
import os
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    ========================================
    📧 ADAPTER FOR NORMAL LOGIN (Username/Password)
    ========================================
    
    What does this do?
    When user logs in with username/password, send them to React home page.
    
    Note: This is NOT used for Google login!
    Google login uses CustomSocialAccountAdapter below.
    """

    def get_login_redirect_url(self, request):
        # After normal login, send user to React home page
        return f"{FRONTEND_URL}/home"


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    ========================================
    🔵 ADAPTER FOR GOOGLE LOGIN (OAuth)
    ========================================
    
    What does this do?
    After user logs in with Google, this generates JWT tokens and
    redirects them to React with the tokens in the URL.
    
    Flow:
    1. User logs in with Google ✅
    2. This adapter runs
    3. Generate JWT tokens (access + refresh)
    4. Build URL: https://your-app.vercel.app/auth/google/callback?access=TOKEN1&refresh=TOKEN2
    5. Redirect user to that URL
    6. React's GoogleCallback.jsx saves the tokens
    7. User is logged in! ✅
    """
    
    def get_login_redirect_url(self, request):
        print("🔥 SOCIAL ADAPTER - Generating JWT tokens for Google login")
        print(f"   - User: {request.user if hasattr(request, 'user') else 'No user'}")
        print(f"   - Is authenticated: {request.user.is_authenticated if hasattr(request, 'user') else False}")
        
        try:
            # Check if user is logged in
            if hasattr(request, 'user') and request.user and request.user.is_authenticated:
                # ✅ User is logged in! Generate JWT tokens
                
                # Create refresh token (long-lived, ~7 days)
                refresh = RefreshToken.for_user(request.user)
                
                # Get access token from refresh token (short-lived, ~24 hours)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                # Build the redirect URL with tokens
                # Example: https://your-app.vercel.app/auth/google/callback?access=TOKEN1&refresh=TOKEN2&user_id=123&username=john
                redirect_url = (
                    f"{FRONTEND_URL}/auth/google/callback"
                    f"?access={access_token}&refresh={refresh_token}"
                    f"&user_id={request.user.id}&username={request.user.username}"
                )
                
                print(f"✅ Redirecting to React with JWT tokens")
                print(f"   - Access token length: {len(access_token)} characters")
                print(f"   - Refresh token length: {len(refresh_token)} characters")
                print(f"   - Redirect URL: {redirect_url[:80]}...")
                
                return redirect_url
            else:
                # ❌ User is NOT logged in - something went wrong
                print("⚠️ User not authenticated or not available")
                return f"{FRONTEND_URL}/login?error=auth_failed"
                
        except Exception as e:
            # ❌ ERROR! Something went wrong
            print(f"❌ Error in adapter: {e}")
            import traceback
            print(traceback.format_exc())
            return f"{FRONTEND_URL}/login?error=adapter_error"
