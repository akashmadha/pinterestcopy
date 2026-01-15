






# pinterest_App/urls.py (APP LEVEL)
# 
# 🔧 GOOGLE OAUTH REDIRECT LOOP FIX SUMMARY:
# ==========================================
# 
# ORIGINAL PROBLEM:
# - User clicks Google login → redirects to Google → Google redirects back
# - But then Django would redirect back to Google again (infinite loop!)
# - The callback URL /api/accounts/google/login/callback/ wasn't properly handled
# 
# ROOT CAUSE:
# - Allauth's default callback behavior was causing redirects back to the login URL
# - Token storage was inconsistent (some places used "access_token", others "accessToken")
# - React routing had duplicate callback routes with different components
# 
# SOLUTION IMPLEMENTED:
# 1. Custom callback view intercepts allauth's callback URL (line 19)
# 2. Lets allauth handle OAuth, then generates JWT tokens
# 3. Redirects to React with tokens as URL parameters
# 4. Fixed token storage consistency across frontend
# 5. Fixed React routing conflicts
# 
# KEY FILES MODIFIED:
# - Backend/pinterest_App/urls.py (this file) - Custom callback URL override
# - Backend/pinterest_App/views.py - Custom callback view implementation  
# - Backend/Backend/settings.py - Added FRONTEND_URL, fixed LOGIN_REDIRECT_URL
# - Frontend/src/Component/GoogleCallback.jsx - Fixed token storage naming
# - Frontend/src/utils/auth.js - Fixed token checking consistency
# - Frontend/src/App.js - Fixed duplicate routing conflicts

from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ========== AUTH ENDPOINTS ==========
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.check_auth, name='profile'),
    path('check-auth/', views.check_auth, name='check_auth'),
    path('current-user/', views.get_current_user, name='current-user'),
    
    # ========== IMAGE ENDPOINTS ==========
    path('save/', views.save_image, name='save-image'),
    path('saved/', views.get_saved_images, name='saved-images'),
    
    # ========== GOOGLE OAUTH ==========
    # Custom JWT endpoint for Google OAuth success
    path(
        "accounts/google/jwt/",
        views.google_login_success,
        name="google_jwt",
    ),
    
    # Test endpoint to debug OAuth flow
    path(
        "test-google-auth/",
        views.test_google_auth,
        name="test_google_auth",
    ),
    # ========== JWT TOKENS ==========
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]