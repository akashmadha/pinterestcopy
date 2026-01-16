#!/usr/bin/env python
"""
🔧 Production Google OAuth Configuration Fixer for Render
==========================================================

This script MUST be run on your Render deployment to fix the OAuth redirect loop.

Run this on Render using the Shell:
    python fix_production_oauth.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.contrib.sites.models import Site
from django.conf import settings


def main():
    print("\n" + "="*70)
    print("🔧 PRODUCTION OAUTH FIX FOR RENDER")
    print("="*70)
    
    # Force production domain
    production_domain = "pinterestcopy.onrender.com"
    
    print(f"\n📍 Setting Site domain to: {production_domain}")
    
    try:
        # Get or create Site
        site, created = Site.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={'domain': production_domain, 'name': 'Pinterest Copy'}
        )
        
        # Update domain
        if site.domain != production_domain:
            old_domain = site.domain
            site.domain = production_domain
            site.save()
            print(f"✅ Updated: {old_domain} → {production_domain}")
        else:
            print(f"✅ Already correct: {production_domain}")
        
        print("\n" + "="*70)
        print("📋 GOOGLE CLOUD CONSOLE - AUTHORIZED REDIRECT URIS")
        print("="*70)
        print("\nMake sure these URIs are added in Google Cloud Console:")
        print("(https://console.cloud.google.com/apis/credentials)")
        print()
        print(f"   1. https://{production_domain}/accounts/google/login/callback/")
        print(f"   2. https://{production_domain}/api/accounts/google/login/callback/")
        
        print("\n" + "="*70)
        print("✅ SITE DOMAIN FIXED!")
        print("="*70)
        print("\n📝 Next Steps:")
        print("   1. Verify the redirect URIs above are in Google Cloud Console")
        print("   2. Restart your Render service")
        print("   3. Test Google login again")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
