from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Fix Google OAuth configuration - remove old Social Apps and use environment variables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🔧 Fixing Google OAuth Configuration...\n'))
        
        # Step 1: Delete all existing Google Social Apps
        old_apps = SocialApp.objects.filter(provider='google')
        if old_apps.exists():
            count = old_apps.count()
            for app in old_apps:
                self.stdout.write(f'   Deleting old Google app: {app.client_id}')
                app.delete()
            self.stdout.write(self.style.SUCCESS(f'✅ Deleted {count} old Google OAuth app(s)\n'))
        else:
            self.stdout.write('   No old Google apps found\n')
        
        # Step 2: Get credentials from environment variables
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR('❌ GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set in environment!'))
            self.stdout.write('   Please set these in your Render dashboard.')
            return
        
        self.stdout.write(f'   Found GOOGLE_CLIENT_ID: {client_id[:20]}...')
        
        # Step 3: Create new Social App with environment variables
        site = Site.objects.get(id=settings.SITE_ID)
        
        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            # Update existing app
            social_app.client_id = client_id
            social_app.secret = client_secret
            social_app.save()
            self.stdout.write(self.style.SUCCESS('✅ Updated existing Google OAuth app'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Created new Google OAuth app'))
        
        # Step 4: Link to site
        social_app.sites.add(site)
        
        # Step 5: Show configuration
        self.stdout.write(self.style.WARNING('\n📋 Current Configuration:'))
        self.stdout.write(f'   Provider: {social_app.provider}')
        self.stdout.write(f'   Client ID: {social_app.client_id}')
        self.stdout.write(f'   Secret: {social_app.secret[:10]}...')
        self.stdout.write(f'   Sites: {", ".join([s.domain for s in social_app.sites.all()])}')
        
        self.stdout.write(self.style.WARNING('\n🔗 OAuth Callback URL:'))
        self.stdout.write(f'   {settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}://{site.domain}/api/accounts/google/login/callback/')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Google OAuth configuration fixed!'))
        self.stdout.write(self.style.WARNING('\n⚠️  IMPORTANT: Add this redirect URI to Google Cloud Console:'))
        self.stdout.write(f'   {settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}://{site.domain}/api/accounts/google/login/callback/')
        self.stdout.write(self.style.WARNING('\n   Then wait 10 minutes and test again.\n'))
