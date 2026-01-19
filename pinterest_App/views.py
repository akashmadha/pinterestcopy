from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from rest_framework import viewsets, permissions, status
import json

# ----------------------------
# User Registration
# ----------------------------
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        print(f"📝 Registration attempt - Username: {username}, Email: {email}")

        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already taken"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        # ✅ Return tokens after registration so user is automatically logged in
        refresh = RefreshToken.for_user(user)
        print(f"✅ User registered successfully: {username} (ID: {user.id})")
        
        return Response({
            "message": "Registration successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=201)

    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return Response({"message": f"Error: {str(e)}"}, status=400)


# ----------------------------
# User Login - Returns JWT tokens
# ----------------------------
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):

    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        print(f"🔐 Login attempt - Username: {username}")
        
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            print(f"✅ Login successful: {username} (ID: {user.id})")
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            print(f"❌ Login failed: Invalid credentials for {username}")
            return Response({'error': 'Invalid credentials'}, status=400)
    
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return Response({'error': 'Login failed'}, status=400)


# ----------------------------
# Logout (optional, frontend can just delete tokens)
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    print(f"🚪 User logging out: {request.user} (ID: {request.user.id})")
    # For JWT, logout is client-side: delete tokens
    return Response({'message': 'Logged out successfully'})


# ----------------------------
# Debug User Info - ADD THIS
# ----------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def debug_user(request):
    print(f"🔍 Debug user request - User: {request.user} (ID: {request.user.id})")
    return Response({
        "user_id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
        "is_authenticated": request.user.is_authenticated
    })


# ----------------------------
# Post ViewSet (Optional CRUD)
# ----------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.AllowAny]


# ----------------------------
# Check Authentication Status
# ----------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_auth(request):
    print(f"🔒 Auth check - User: {request.user} (ID: {request.user.id})")
    return Response({
        "message": "Authenticated",
        "user": request.user.username,
        "email": request.user.email,
        "user_id": request.user.id
    })







from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Image, SavedImage
from .serializers import ImageSerializer, SavedImageSerializer

# Google OAuth imports
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from urllib.parse import urlencode

# -----------------------------
# 1) Save Image (POST)
# -----------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_image(request):
    user = request.user

    image_url = request.data.get("image_url")
    title = request.data.get("title", "")
    external_id = request.data.get("external_id", None)
    source = request.data.get("source", "")

    if not image_url:
        return Response({"error": "image_url is required"}, status=400)

    # 1. Check if this image already exists in DB
    image, created = Image.objects.get_or_create(
        image_url=image_url,
        defaults={
            "title": title,
            "external_id": external_id,
            "source": source
        }
    )

    # 2. Create SavedImage (or ignore if already saved)
    saved, created_link = SavedImage.objects.get_or_create(
        user=user,
        image=image
    )

    if created_link:
        return Response({"message": "Image saved!"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Already saved!"}, status=status.HTTP_200_OK)







# -----------------------------------------
# 2) Get all saved images of the user (GET)
# -----------------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_saved_images(request):
    user = request.user
    
    saved_images = SavedImage.objects.filter(user=user).select_related("image")
    serializer = SavedImageSerializer(saved_images, many=True)
    
    return Response(serializer.data)

# views.py - Keep it simple
from django.http import JsonResponse
from django.middleware.csrf import get_token





def get_current_user(request):
    """API endpoint that React calls after redirect"""
    if request.user.is_authenticated:
        return JsonResponse({
            'isAuthenticated': True,
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'firstName': request.user.first_name,
            'lastName': request.user.last_name,
        })
    return JsonResponse({
        'isAuthenticated': False,
        'message': 'Not authenticated'
    })



def get_csrf_token(request):
    """Get CSRF token for React if needed"""
    return JsonResponse({'csrfToken': get_token(request)})


from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

def google_login_success(request):
    """
    This view is called after successful Google OAuth.
    It generates JWT tokens and redirects to React with the tokens.
    """
    print(f"🔥 Google login success view called")
    print(f"   - User: {request.user}")
    print(f"   - Is authenticated: {request.user.is_authenticated}")
    print(f"   - Request method: {request.method}")
    print(f"   - Request path: {request.path}")
    
    if not request.user.is_authenticated:
        print("❌ User not authenticated, redirecting to login")
        return redirect(f"{settings.FRONTEND_URL}/login?error=auth_failed")

    # Generate JWT tokens for the authenticated user
    refresh = RefreshToken.for_user(request.user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    print(f"✅ Generated tokens for user: {request.user.username} (ID: {request.user.id})")
    print(f"   - Access token length: {len(access_token)}")
    print(f"   - Refresh token length: {len(refresh_token)}")
    
    # Redirect to React with tokens as URL parameters
    redirect_url = (
        f"{settings.FRONTEND_URL}/auth/google/callback"
        f"?access={access_token}&refresh={refresh_token}"
        f"&user_id={request.user.id}&username={request.user.username}"
    )
    
    print(f"🔄 Redirecting to: {redirect_url[:100]}...")
    return redirect(redirect_url)


@api_view(['GET'])
@permission_classes([AllowAny])
def test_google_auth(request):
    """Test endpoint to debug Google OAuth flow"""
    print(f"🧪 Test Google Auth endpoint called")
    print(f"   - User: {request.user}")
    print(f"   - Is authenticated: {request.user.is_authenticated}")
    
    # Show the exact callback URL that Django will use
    from django.urls import reverse
    from django.conf import settings
    from allauth.socialaccount.providers.google.provider import GoogleProvider
    
    try:
        callback_url = request.build_absolute_uri(reverse('google_oauth2_callback'))
        print(f"   - Callback URL: {callback_url}")
    except Exception as e:
        callback_url = f"Could not determine callback URL: {str(e)}"
    
    # Get Google OAuth settings
    google_settings = settings.SOCIALACCOUNT_PROVIDERS.get('google', {})
    app_config = google_settings.get('APP', {})
    
    # Check if SocialApp exists in database
    from allauth.socialaccount.models import SocialApp
    try:
        social_apps = SocialApp.objects.filter(provider='google')
        social_app_info = []
        for app in social_apps:
            social_app_info.append({
                'client_id': app.client_id[:30] + '...',
                'sites': [s.domain for s in app.sites.all()]
            })
    except Exception as e:
        social_app_info = f"Error: {str(e)}"
    
    return JsonResponse({
        'status': 'debug',
        'user_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None,
        'callback_url': callback_url,
        'settings_client_id': app_config.get('client_id', 'NOT SET')[:30] + '...' if app_config.get('client_id') else 'NOT SET',
        'settings_has_secret': bool(app_config.get('secret')),
        'database_social_apps': social_app_info,
        'frontend_url': settings.FRONTEND_URL,
        'site_id': settings.SITE_ID,
        'account_default_http_protocol': settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL,
        'debug_mode': settings.DEBUG,
    })


# Signal handlers removed - they were causing errors by accessing user before it was created


def custom_google_callback(request):
    """
    ========================================
    🔧 CUSTOM GOOGLE OAUTH CALLBACK HANDLER
    ========================================
    
    Simple Explanation:
    This is the MOST IMPORTANT function for Google login!
    When Google sends the user back after login, this function:
    1. Receives the user from Google
    2. Lets Django authenticate them
    3. Generates JWT tokens
    4. Sends them to React with the tokens
    
    Why do we need this?
    Without this custom handler, Django would just redirect to /home
    without giving React the JWT tokens. Then React wouldn't know
    the user is logged in!
    
    Flow:
    1. User logs in with Google ✅
    2. Google sends them back to: /api/accounts/google/login/callback/?code=ABC123
    3. THIS FUNCTION runs
    4. Django processes the code and logs in the user
    5. We generate JWT tokens
    6. We redirect to React with tokens: /auth/google/callback?access=TOKEN1&refresh=TOKEN2
    7. React saves tokens and user is logged in! ✅
    """
    print("🔥 CUSTOM GOOGLE CALLBACK - Starting OAuth processing")
    print(f"   - URL parameters: {dict(request.GET)}")
    print(f"   - User before OAuth: {request.user}")
    print(f"   - Is authenticated before: {request.user.is_authenticated}")
    
    try:
        # Import Django-allauth's Google callback handler
        from allauth.socialaccount.providers.google.views import oauth2_callback
        
        # ========================================
        # STEP 1: Let Django-allauth handle the OAuth process
        # ========================================
        # This does the heavy lifting:
        # - Validates the code from Google
        # - Gets user info from Google (email, name, etc.)
        # - Creates or gets the user in our database
        # - Logs them in
        response = oauth2_callback(request)
        
        print(f"   - User after OAuth: {request.user}")
        print(f"   - Is authenticated after: {request.user.is_authenticated}")
        print(f"   - Response type: {type(response)}")
        print(f"   - Response status: {response.status_code if hasattr(response, 'status_code') else 'N/A'}")
        
        # ========================================
        # STEP 2: Check if user is authenticated
        # ========================================
        if request.user.is_authenticated:
            print("✅ User authenticated successfully!")
            print(f"   - Username: {request.user.username}")
            print(f"   - Email: {request.user.email}")
            print(f"   - User ID: {request.user.id}")
            
            # ========================================
            # STEP 3: Generate JWT tokens
            # ========================================
            # These tokens are like digital keys that prove the user is logged in
            refresh = RefreshToken.for_user(request.user)
            access_token = str(refresh.access_token)   # Short-lived (~24 hours)
            refresh_token = str(refresh)                # Long-lived (~7 days)
            
            print(f"   - Generated access token: {len(access_token)} characters")
            print(f"   - Generated refresh token: {len(refresh_token)} characters")
            
            # ========================================
            # STEP 4: Build redirect URL with tokens
            # ========================================
            # Send user to React with tokens in the URL
            # React will grab these tokens and save them
            redirect_url = (
                f"{settings.FRONTEND_URL}/auth/google/callback"
                f"?access={access_token}&refresh={refresh_token}"
                f"&user_id={request.user.id}&username={request.user.username}"
            )
            
            print(f"🔄 Redirecting to React with tokens")
            print(f"   - URL: {redirect_url[:100]}...")
            
            return redirect(redirect_url)
        
        # ========================================
        # STEP 2B: User not authenticated - check if redirect needed
        # ========================================
        # Sometimes Django-allauth needs to redirect to complete signup
        if hasattr(response, 'status_code') and response.status_code in [301, 302, 303, 307, 308]:
            print(f"⚠️ Django-allauth returned redirect")
            print(f"   - Location: {response.get('Location', 'unknown')}")
            # Follow the redirect - allauth might need to complete signup
            return response
        
        # ========================================
        # ERROR: Authentication failed
        # ========================================
        print("❌ Authentication failed - user not logged in")
        return redirect(f"{settings.FRONTEND_URL}/login?error=auth_failed")
        
    except Exception as e:
        # ========================================
        # ERROR: Something went wrong
        # ========================================
        print(f"❌ Error in custom_google_callback: {str(e)}")
        print(f"   - Exception type: {type(e)}")
        import traceback
        print(f"   - Full traceback:")
        print(traceback.format_exc())
        
        # Send user back to login with error message
        return redirect(f"{settings.FRONTEND_URL}/login?error=oauth_error")




