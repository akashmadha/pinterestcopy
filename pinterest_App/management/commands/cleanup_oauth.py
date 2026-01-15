from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Clean up orphaned OAuth data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🧹 Cleaning up OAuth data...\n'))
        
        # Find and delete orphaned SocialAccounts (accounts without users)
        orphaned = []
        for account in SocialAccount.objects.all():
            try:
                # Try to access the user
                _ = account.user
            except:
                # This account has no user - it's orphaned
                orphaned.append(account)
        
        if orphaned:
            self.stdout.write(f'   Found {len(orphaned)} orphaned SocialAccount(s)')
            for account in orphaned:
                self.stdout.write(f'   Deleting orphaned account: {account.provider} - {account.uid}')
                account.delete()
            self.stdout.write(self.style.SUCCESS(f'✅ Deleted {len(orphaned)} orphaned SocialAccount(s)'))
        else:
            self.stdout.write('   No orphaned SocialAccounts found')
        
        # Show all users
        users = User.objects.all()
        self.stdout.write(f'\n📊 Total users in database: {users.count()}')
        for user in users:
            social_accounts = SocialAccount.objects.filter(user=user)
            self.stdout.write(f'   - {user.username} (ID: {user.id}) - {social_accounts.count()} social account(s)')
        
        # Show all SocialApps
        social_apps = SocialApp.objects.all()
        self.stdout.write(f'\n📱 Total SocialApps: {social_apps.count()}')
        for app in social_apps:
            self.stdout.write(f'   - {app.provider}: {app.client_id[:30]}...')
            self.stdout.write(f'     Sites: {", ".join([s.domain for s in app.sites.all()])}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Cleanup complete!\n'))
