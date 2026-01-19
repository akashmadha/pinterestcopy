# ========================================
# 📱 APP-LEVEL URL CONFIGURATION
# ========================================
#
# Simple Explanation:
# This file defines URLs for the pinterest_App.
# All these URLs are prefixed with /api/ (defined in Backend/urls.py)
#
# Examples:
# - /api/register/ → register view
# - /api/login/ → login_view
# - /api/save/ → save_image view
#

from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ========================================
    # 👤 USER AUTHENTICATION ENDPOINTS
    # ========================================
    path('register/', views.register, name='register'),           # Create new account
    path('login/', views.login_view, name='login'),               # Login with username/password
    path('logout/', views.logout, name='logout'),                 # Logout
    path('profile/', views.check_auth, name='profile'),           # Get user profile
    path('check-auth/', views.check_auth, name='check_auth'),     # Check if user is logged in
    path('current-user/', views.get_current_user, name='current-user'),  # Get current user info
    
    # ========================================
    # 🖼️ IMAGE MANAGEMENT ENDPOINTS
    # ========================================
    path('save/', views.save_image, name='save-image'),           # Save an image
    path('saved/', views.get_saved_images, name='saved-images'),  # Get all saved images
    
    # ========================================
    # 🔵 GOOGLE OAUTH ENDPOINTS
    # ========================================
    
    # Custom callback handler (registered here for reference)
    # The actual URL is in Backend/urls.py to ensure it comes before allauth URLs
    path(
        "accounts/google/login/callback/",
        views.custom_google_callback,
        name="google_callback_custom",
    ),
    
    # JWT generation endpoint (alternative to adapter)
    # This is called if LOGIN_REDIRECT_URL points here
    path(
        "accounts/google/jwt/",
        views.google_login_success,
        name="google_jwt",
    ),
    
    # Test endpoint to debug OAuth configuration
    # Visit: https://pinterestcopy.onrender.com/api/test-google-auth/
    path(
        "test-google-auth/",
        views.test_google_auth,
        name="test_google_auth",
    ),
    
    # ========================================
    # 🔑 JWT TOKEN ENDPOINTS
    # ========================================
    # These are for manual token management (not used by Google OAuth)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Get new tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # Refresh access token
]
