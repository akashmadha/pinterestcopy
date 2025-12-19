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
from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.dispatch import receiver

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
    
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)
        return JsonResponse({
            'status': 'success',
            'user': request.user.username,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User not authenticated'
        })


# Signal handlers for debugging Google OAuth flow
@receiver(pre_social_login)
def debug_pre_social_login(sender, request, sociallogin, **kwargs):
    print("🔥 PRE_SOCIAL_LOGIN signal received")
    print(f"   - User: {sociallogin.user}")
    print(f"   - Account: {sociallogin.account}")


@receiver(social_account_added)
def debug_social_account_added(sender, request, sociallogin, **kwargs):
    print("🔥 SOCIAL_ACCOUNT_ADDED signal received")
    print(f"   - User: {sociallogin.user}")
    print(f"   - Account: {sociallogin.account}")
    
    # This is where we can redirect after successful social login
    # But signals don't allow us to return a redirect response


def custom_google_callback(request):
    """
    🔧 MAIN FIX: Custom Google OAuth callback that intercepts the allauth flow
    
    PROBLEM SOLVED: The original issue was a redirect loop where:
    1. User clicks Google login → /api/accounts/google/login/
    2. Redirects to Google → User authenticates
    3. Google redirects back → /api/accounts/google/login/callback/
    4. Allauth processes OAuth but then redirects back to step 1 (LOOP!)
    
    SOLUTION: This custom view intercepts the callback URL and:
    1. Lets allauth handle the OAuth authentication process
    2. After successful auth, generates JWT tokens
    3. Redirects to React with tokens (breaking the loop)
    
    This prevents the infinite redirect loop by providing a proper exit point.
    """
    print("🔥 CUSTOM GOOGLE CALLBACK called")
    print(f"   - GET params: {dict(request.GET)}")
    print(f"   - User before: {request.user}")
    print(f"   - Is authenticated before: {request.user.is_authenticated}")
    
    # Import allauth's Google callback view
    from allauth.socialaccount.providers.google.views import oauth2_callback
    
    # 🔧 STEP 1: Let allauth handle the OAuth process (user authentication)
    response = oauth2_callback(request)
    
    print(f"   - User after allauth: {request.user}")
    print(f"   - Is authenticated after: {request.user.is_authenticated}")
    print(f"   - Response status: {response.status_code}")
    
    # 🔧 STEP 2: If allauth processed successfully and user is authenticated
    if request.user.is_authenticated:
        print("✅ User authenticated by allauth, generating JWT tokens")
        
        # 🔧 STEP 3: Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(request.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # 🔧 STEP 4: Redirect to React with tokens (BREAKS THE LOOP!)
        # Instead of redirecting back to Django, we go to React with tokens
        redirect_url = (
            f"{settings.FRONTEND_URL}/auth/google/callback"
            f"?access={access_token}&refresh={refresh_token}"
            f"&user_id={request.user.id}&username={request.user.username}"
        )
        
        print(f"🔄 Redirecting to React: {redirect_url[:100]}...")
        return redirect(redirect_url)
    
    # If authentication failed, return the original allauth response
    print("❌ Authentication failed, returning original response")
    return response




