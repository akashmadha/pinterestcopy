from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Fix Django Site domain for Google OAuth'

    def handle(self, *args, **options):
        # Get or create Site with ID=1
        site, created = Site.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': 'pinterestcopy.onrender.com',
                'name': 'Pinterest Copy'
            }
        )
        
        if not created:
            # Update existing site
            site.domain = 'pinterestcopy.onrender.com'
            site.name = 'Pinterest Copy'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Updated Site: {site.domain}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Created Site: {site.domain}'))
        
        # Show current configuration
        self.stdout.write(self.style.WARNING('\n📋 Current Configuration:'))
        self.stdout.write(f'   Site ID: {site.id}')
        self.stdout.write(f'   Site Domain: {site.domain}')
        self.stdout.write(f'   Site Name: {site.name}')
        self.stdout.write(f'   Protocol: {settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}')
        self.stdout.write(f'\n🔗 OAuth Callback URL will be:')
        self.stdout.write(f'   {settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL}://{site.domain}/api/accounts/google/login/callback/')
