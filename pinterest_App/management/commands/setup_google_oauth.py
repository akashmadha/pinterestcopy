from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Setup Google OAuth SocialApp in database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🔧 Setting up Google OAuth...\n'))
        
        # Get credentials from environment variables
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            self.stdout.write(self.style.ERROR('❌ ERROR: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set!'))
            self.stdout.write('   Please set these environment variables in Render dashboard.')
            return
        
        self.stdout.write(f'   Found GOOGLE_CLIENT_ID: {client_id[:30]}...')
        self.stdout.write(f'   Found GOOGLE_CLIENT_SECRET: {client_secret[:10]}...')
        
        # Get or create the Site
        site = Site.objects.get(id=settings.SITE_ID)
        self.stdout.write(f'   Site: {site.domain}')
        
        # Delete any existing Google SocialApps
        old_apps = SocialApp.objects.filter(provider='google')
        if old_apps.exists():
            count = old_apps.count()
            for app in old_apps:
                self.stdout.write(f'   Deleting old Google app: {app.client_id}')
                app.delete()
            self.stdout.write(self.style.SUCCESS(f'✅ Deleted {count} old Google OAuth app(s)'))
        
        # Create new SocialApp
        social_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=client_secret,
        )
        
        # Link to site
        social_app.sites.add(site)
        
        self.stdout.write(self.style.SUCCESS('\n✅ Google OAuth SocialApp created successfully!'))
        
        # Show configuration
        self.stdout.write(self.style.WARNING('\n📋 Configuration:'))
        self.stdout.write(f'   Provider: {social_app.provider}')
        self.stdout.write(f'   Client ID: {social_app.client_id}')
        self.stdout.write(f'   Secret: {social_app.secret[:15]}...')
        self.stdout.write(f'   Sites: {", ".join([s.domain for s in social_app.sites.all()])}')
        
        self.stdout.write(self.style.WARNING('\n🔗 OAuth URLs:'))
        self.stdout.write(f'   Login: {settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}://{site.domain}/accounts/google/login/')
        self.stdout.write(f'   Callback: {settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}://{site.domain}/accounts/google/login/callback/')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Setup complete! You can now test Google OAuth.\n'))
