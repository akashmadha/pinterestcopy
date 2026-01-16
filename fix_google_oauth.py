#!/usr/bin/env python
"""
🔧 Google OAuth Configuration Fixer
====================================

This script fixes the Google OAuth redirect loop issue by:
1. Checking and fixing the Site domain in the database
2. Verifying Google OAuth app configuration
3. Showing the correct redirect URIs to add in Google Cloud Console

Run this script after deployment to ensure OAuth is configured correctly.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings


def fix_site_domain():
    """Fix the Site domain to match the current environment"""
    print("\n" + "="*60)
    print("🔧 FIXING SITE DOMAIN")
    print("="*60)
    
    # Determine correct domain
    if os.environ.get("RENDER"):
        domain = "pinterestcopy.onrender.com"
        protocol = "https"
    else:
        domain = "localhost:8000"
        protocol = "http"
    
    # Get or create Site
    site, created = Site.objects.get_or_create(
        id=settings.SITE_ID,
        defaults={'domain': domain, 'name': 'Pinterest Copy'}
    )
    
    # Update if needed
    if site.domain != domain:
        old_domain = site.domain
        site.domain = domain
        site.save()
        print(f"✅ Updated Site domain: {old_domain} → {domain}")
    else:
        print(f"✅ Site domain already correct: {domain}")
    
    return domain, protocol


def check_social_app():
    """Check if Google SocialApp is configured in database"""
    print("\n" + "="*60)
    print("🔍 CHECKING GOOGLE OAUTH APP CONFIGURATION")
    print("="*60)
    
    try:
        apps = SocialApp.objects.filter(provider='google')
        
        if not apps.exists():
            print("⚠️  No Google SocialApp found in database")
            print("   This is OK if you're using settings.py configuration")
            return None
        
        for app in apps:
            print(f"\n✅ Found Google SocialApp:")
            print(f"   - Client ID: {app.client_id[:30]}...")
            print(f"   - Has Secret: {'Yes' if app.secret else 'No'}")
            print(f"   - Sites: {[s.domain for s in app.sites.all()]}")
            
            # Check if current site is linked
            current_site = Site.objects.get(id=settings.SITE_ID)
            if current_site not in app.sites.all():
                print(f"\n⚠️  WARNING: Current site '{current_site.domain}' is not linked to this app!")
                print(f"   Adding site to app...")
                app.sites.add(current_site)
                print(f"   ✅ Site added successfully")
            
        return apps.first()
    
    except Exception as e:
        print(f"❌ Error checking SocialApp: {e}")
        return None


def show_redirect_uris(domain, protocol):
    """Show the correct redirect URIs for Google Cloud Console"""
    print("\n" + "="*60)
    print("📋 GOOGLE CLOUD CONSOLE CONFIGURATION")
    print("="*60)
    
    print("\n🔗 Add these Authorized Redirect URIs in Google Cloud Console:")
    print("   (https://console.cloud.google.com/apis/credentials)")
    print()
    
    # The correct redirect URIs
    redirect_uris = [
        f"{protocol}://{domain}/accounts/google/login/callback/",
        f"{protocol}://{domain}/api/accounts/google/login/callback/",
    ]
    
    for uri in redirect_uris:
        print(f"   ✅ {uri}")
    
    print("\n⚠️  IMPORTANT: Both URIs should be added to handle different URL patterns")
    
    # Show current settings
    print("\n" + "="*60)
    print("⚙️  CURRENT DJANGO SETTINGS")
    print("="*60)
    print(f"   - SITE_ID: {settings.SITE_ID}")
    print(f"   - Site Domain: {domain}")
    print(f"   - Protocol: {protocol}")
    print(f"   - FRONTEND_URL: {settings.FRONTEND_URL}")
    print(f"   - DEBUG: {settings.DEBUG}")
    
    # Show Google OAuth settings from settings.py
    google_config = settings.SOCIALACCOUNT_PROVIDERS.get('google', {})
    app_config = google_config.get('APP', {})
    
    print("\n📱 Google OAuth Settings (from settings.py):")
    client_id = app_config.get('client_id', 'NOT SET')
    if client_id and client_id != 'NOT SET':
        print(f"   - Client ID: {client_id[:30]}...")
    else:
        print(f"   - Client ID: {client_id}")
    print(f"   - Has Secret: {'Yes' if app_config.get('secret') else 'No'}")
    print(f"   - OAUTH_PKCE_ENABLED: {google_config.get('OAUTH_PKCE_ENABLED', False)}")


def test_oauth_flow():
    """Show the OAuth flow URLs"""
    print("\n" + "="*60)
    print("🔄 OAUTH FLOW URLS")
    print("="*60)
    
    domain = Site.objects.get(id=settings.SITE_ID).domain
    protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL
    
    print("\n1️⃣  User clicks 'Login with Google' button:")
    print(f"   → Frontend redirects to: {protocol}://{domain}/api/accounts/google/login/")
    
    print("\n2️⃣  Django redirects to Google OAuth:")
    print(f"   → Google login page with redirect_uri parameter")
    
    print("\n3️⃣  User logs in with Google:")
    print(f"   → Google redirects back to: {protocol}://{domain}/accounts/google/login/callback/")
    print(f"   → OR: {protocol}://{domain}/api/accounts/google/login/callback/")
    
    print("\n4️⃣  Django processes OAuth and generates JWT:")
    print(f"   → Redirects to: {settings.FRONTEND_URL}/auth/google/callback?access=...&refresh=...")
    
    print("\n5️⃣  React saves tokens and redirects to home:")
    print(f"   → User is logged in! ✅")


def main():
    """Main function to run all fixes and checks"""
    print("\n" + "="*60)
    print("🚀 GOOGLE OAUTH CONFIGURATION FIXER")
    print("="*60)
    
    try:
        # Fix site domain
        domain, protocol = fix_site_domain()
        
        # Check social app configuration
        check_social_app()
        
        # Show redirect URIs
        show_redirect_uris(domain, protocol)
        
        # Show OAuth flow
        test_oauth_flow()
        
        print("\n" + "="*60)
        print("✅ CONFIGURATION CHECK COMPLETE")
        print("="*60)
        print("\n📝 Next Steps:")
        print("   1. Copy the redirect URIs shown above")
        print("   2. Add them to Google Cloud Console")
        print("   3. Restart your Django server")
        print("   4. Test the Google login flow")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
