# ========================================
# 🌐 MAIN URL CONFIGURATION
# ========================================
#
# Simple Explanation:
# This file tells Django which URLs go to which views.
# Think of it as a "phone book" for your website.
#
# CRITICAL FOR GOOGLE LOGIN:
# The ORDER of URLs matters! Our custom callback MUST come
# BEFORE the allauth URLs, otherwise allauth will handle
# the callback and won't generate JWT tokens.
#

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from pinterest_App import views

def home(request):
    """Simple home page showing the backend is running"""
    return HttpResponse("<h1>Pinterest Clone Backend Running Successfully</h1>")


urlpatterns = [
    # ========================================
    # 🏠 HOME & ADMIN
    # ========================================
    path('', home),                    # Root URL: https://pinterestcopy.onrender.com/
    path('admin/', admin.site.urls),   # Admin panel: https://pinterestcopy.onrender.com/admin/
    
    # ========================================
    # 🔧 CRITICAL: CUSTOM GOOGLE OAUTH CALLBACK
    # ========================================
    # This MUST come BEFORE allauth URLs!
    # 
    # Why? When Google sends user back after login, Django checks URLs from top to bottom.
    # If we put this AFTER allauth URLs, allauth will handle it and won't generate JWT tokens.
    # 
    # URL: https://pinterestcopy.onrender.com/api/accounts/google/login/callback/
    # Handler: views.custom_google_callback (in pinterest_App/views.py)
    #
    path('api/accounts/google/login/callback/', 
         views.custom_google_callback, 
         name='google_callback_override'),
    
    # ========================================
    # 📱 APP URLs (Login, Register, Images, etc.)
    # ========================================
    # All URLs starting with /api/ go to pinterest_App/urls.py
    # Examples:
    # - /api/login/
    # - /api/register/
    # - /api/save/
    # - /api/saved/
    path('api/', include('pinterest_App.urls')),
    
    # ========================================
    # 🔵 DJANGO-ALLAUTH URLs (Google OAuth)
    # ========================================
    # These handle the Google OAuth flow
    # 
    # Two URL patterns for backward compatibility:
    # 1. /accounts/google/login/ - Standard allauth pattern
    # 2. /api/accounts/google/login/ - Our custom pattern
    #
    # Both work, but we use /api/accounts/ for consistency
    path('accounts/', include('allauth.urls')),
    path('api/accounts/', include('allauth.urls')),
]   

