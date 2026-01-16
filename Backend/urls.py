"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from pinterest_App import views

def home(request):
    return HttpResponse("<h1>Pinterest Clone Backend Running Successfully</h1>")


urlpatterns = [
    path('', home),     
    path('admin/', admin.site.urls),
    
    # 🔧 CRITICAL: Custom Google OAuth callback MUST come BEFORE allauth URLs
    # This intercepts the callback and generates JWT tokens
    path('api/accounts/google/login/callback/', views.custom_google_callback, name='google_callback_override'),
    
    # Now include the rest of the app URLs
    path('api/', include('pinterest_App.urls')),
    
    # Add allauth URLs at BOTH root and /api/ level to handle both redirect URIs
    path('accounts/', include('allauth.urls')),
    path('api/accounts/', include('allauth.urls')),  # Also handle /api/accounts/ for backward compatibility
]   

