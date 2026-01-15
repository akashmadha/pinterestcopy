from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    """
    Link social account to existing user if email matches.
    This prevents the "SocialAccount has no user" error.
    """
    print("🔗 PRE_SOCIAL_LOGIN - Linking social account to user")
    
    # If user is already logged in, don't do anything
    if request.user.is_authenticated:
        print(f"   - User already authenticated: {request.user.username}")
        return
    
    # If sociallogin already has a user, don't do anything
    if sociallogin.is_existing:
        print(f"   - Social account already exists and is linked")
        return
    
    # Get the email from the social account
    email = sociallogin.account.extra_data.get('email')
    print(f"   - Email from Google: {email}")
    
    if not email:
        print("   ⚠️ No email provided by Google")
        return
    
    # Check if a user with this email already exists
    try:
        existing_user = User.objects.get(email=email)
        print(f"   - Found existing user: {existing_user.username}")
        
        # Link the social account to the existing user
        sociallogin.connect(request, existing_user)
        print(f"   ✅ Linked social account to existing user")
    except User.DoesNotExist:
        print(f"   - No existing user with email {email}")
        print(f"   - Will create new user")
    except User.MultipleObjectsReturned:
        print(f"   ⚠️ Multiple users with email {email} - using first one")
        existing_user = User.objects.filter(email=email).first()
        sociallogin.connect(request, existing_user)
    except Exception as e:
        print(f"   ❌ Error linking account: {e}")
        import traceback
        print(traceback.format_exc())
