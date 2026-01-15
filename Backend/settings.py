"""
Django settings or Backend project.
"""

from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

if os.environ.get("RENDER"):
    pass  # On Render, environment variables are injected automatically
else:
    from dotenv import load_dotenv
    load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'pinterest_App',
    'rest_framework.authtoken',
     "django_extensions",

     # Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

     # REST Auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'pinterest_App.middleware.DisableCSRFForAPI',  # Custom middleware to exempt API from CSRF
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# 🔧 PRODUCTION FIX: CORS settings for both development and production
CORS_ALLOWED_ORIGINS = [
    # Development URLs
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    
    # Production URLs
    "https://pinterestcopy.onrender.com",  # Backend URL
    "https://pinterestcopy-mkp2.vercel.app",  # Main Vercel URL
    "https://pinterestcopy-mkp2-6vyfhtv24-ngo-linkup.vercel.app",  # Deployment-specific Vercel URL
]

CORS_ALLOW_CREDENTIALS = True

# 🔧 SECURITY: Disable CORS_ALLOW_ALL_ORIGINS in production
# For development: allows all origins (convenient but insecure)
# For production: comment out this line and use CORS_ALLOWED_ORIGINS instead
CORS_ALLOW_ALL_ORIGINS = os.getenv("DEBUG", "False") == "True"

ROOT_URLCONF = 'Backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Backend.wsgi.application'

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ UPDATED JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),  # Increased for debugging
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# ✅ UPDATED REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Disable CSRF for REST API since we're using JWT
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

# 🔧 AUTO-FIX: Update Site domain for Google OAuth
# This ensures the redirect URI matches your actual domain
def fix_site_domain():
    """Automatically fix the Site domain on startup"""
    try:
        from django.contrib.sites.models import Site
        import os
        
        # Determine the correct domain based on environment
        if os.environ.get("RENDER"):
            domain = "pinterestcopy.onrender.com"
        else:
            domain = "localhost:8000"
        
        site, created = Site.objects.get_or_create(
            id=SITE_ID,
            defaults={'domain': domain, 'name': 'Pinterest Copy'}
        )
        
        if site.domain != domain:
            site.domain = domain
            site.save()
            print(f"✅ Updated Site domain to: {domain}")
        else:
            print(f"✅ Site domain already correct: {domain}")
            
        print(f"🔗 OAuth callback URL: {ACCOUNT_DEFAULT_HTTP_PROTOCOL}://{domain}/api/accounts/google/login/callback/")
        
    except Exception as e:
        print(f"⚠️ Could not update Site domain: {e}")
        print("   This is normal on first migration. Will fix on next restart.")

# Call the fix function (will run on Django startup)
import sys
if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
    # Don't run during migrations to avoid database errors
    try:
        fix_site_domain()
    except:
        pass  # Ignore errors during initial setup




ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True

# Session settings for OAuth
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True

# Skip the confirmation page and go directly to Google OAuth
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_STORE_TOKENS = True

# Prevent allauth from trying to redirect to accounts/profile/
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/api/accounts/google/jwt/"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/api/accounts/google/jwt/"

# Skip email confirmation for social accounts
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_UNIQUE_EMAIL = True

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': None,
    'JWT_AUTH_REFRESH_COOKIE': None,
    'JWT_AUTH_HTTPONLY': False,
    'JWT_AUTH_RETURN_EXPIRATION': True,
    'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',
}



# Google OAuth provider settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
       'APP': {
            'client_id': os.getenv("GOOGLE_CLIENT_ID"),
            'secret': os.getenv("GOOGLE_CLIENT_SECRET"),
            'key': ''
        }
    }
}


SOCIALACCOUNT_LOGIN_ON_GET = True


# 🔧 PRODUCTION FIX: CSRF trusted origins for both development and production
CSRF_TRUSTED_ORIGINS = [
    # Development URLs
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://localhost:3000",
    
    # Production URLs - Render Backend
    "https://pinterestcopy.onrender.com",
    
    # Production Vercel URLs
    "https://pinterestcopy-mkp2.vercel.app",
    "https://pinterestcopy-mkp2-6vyfhtv24-ngo-linkup.vercel.app",
]

# 🔧 PRODUCTION FIX: Cookie settings for both development and production
# These settings make cookies work between React and Django
# In production with HTTPS, these should be more secure
SESSION_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'  # 'None' required for cross-site in production
SESSION_COOKIE_SECURE = not DEBUG  # True in production with HTTPS
CSRF_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'
CSRF_COOKIE_SECURE = not DEBUG  # True in production with HTTPS

# For allauth to work properly
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https' if not DEBUG else 'http'

# Exempt API endpoints from CSRF since we're using JWT authentication
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_USE_SESSIONS = False




ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email', 'username*', 'password1*', 'password2*']

ACCOUNT_ADAPTER = "pinterest_App.adapters.CustomAccountAdapter"
SOCIALACCOUNT_ADAPTER = "pinterest_App.adapters.CustomSocialAccountAdapter"

# Debug: Print adapter configuration
print("🔧 ADAPTER CONFIGURATION:")
print(f"   - ACCOUNT_ADAPTER: {ACCOUNT_ADAPTER}")
print(f"   - SOCIALACCOUNT_ADAPTER: {SOCIALACCOUNT_ADAPTER}")

print("🔥 USING Backend.settings 🔥")

# 🔧 PRODUCTION FIX: Frontend URL for redirects - supports both development and production
# For development: uses localhost:3000
# For production: set FRONTEND_URL environment variable to your Vercel domain
# Example: FRONTEND_URL=https://your-app.vercel.app
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

LOGIN_REDIRECT_URL = "/api/accounts/google/jwt/"

LOGOUT_REDIRECT_URL = f"{FRONTEND_URL}/login"