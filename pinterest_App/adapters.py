"""
Custom allauth adapter to handle Google OAuth redirect with JWT tokens.
"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter that redirects Google OAuth users to our JWT token endpoint.
    """
    
    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully connecting
        a social account.
        """
        assert request.user.is_authenticated
        # Redirect to our callback that generates JWT tokens
        return '/api/google/callback/'
    
    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after a successful login.
        """
        # Redirect to our callback that generates JWT tokens
        return '/api/google/callback/'
    
    def is_open_for_signup(self, request, sociallogin):
        """
        Allow automatic signup for social accounts.
        """
        return True
    
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).
        """
        # Auto connect the account
        pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save the user after social login.
        """
        user = super().save_user(request, sociallogin, form)
        return user

