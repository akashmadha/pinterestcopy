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


# -----------------------------------------
# Google OAuth Callback - Returns JWT tokens
# -----------------------------------------
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login

@csrf_exempt
def google_oauth_callback(request):
    """
    Custom callback for Google OAuth that returns JWT tokens.
    This view handles the redirect from Google after authentication.
    """
    try:
        print(f"🔍 Google OAuth callback called. User authenticated: {request.user.is_authenticated}")
        print(f"🔍 Session key: {request.session.session_key}")
        print(f"🔍 User: {request.user if hasattr(request, 'user') else 'No user attribute'}")
        
        # Check if user is authenticated via allauth social account
        if request.user.is_authenticated:
            user = request.user
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            print(f"✅ Google OAuth successful: {user.username} (ID: {user.id})")
            
            # Get frontend URL from settings or use default
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            frontend_url = f"{frontend_url}/google-callback"
            
            tokens = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
                'email': user.email if user.email else ''
            }
            
            # Use URL hash to pass tokens (won't be sent to server)
            redirect_url = f"{frontend_url}#{urlencode(tokens)}"
            print(f"🔀 Redirecting to: {frontend_url}")
            return redirect(redirect_url)
        
        else:
            # User not authenticated, redirect to login
            print("❌ Google OAuth failed: User not authenticated")
            print(f"🔍 Session data: {dict(request.session)}")
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            return redirect(f"{frontend_url}/login?error=oauth_failed")
    
    except Exception as e:
        import traceback
        print(f"❌ Google OAuth callback error: {str(e)}")
        print(f"🔍 Traceback: {traceback.format_exc()}")
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}/login?error={str(e)}")


# -----------------------------------------
# Alternative: API endpoint to get tokens after Google login
# -----------------------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def google_oauth_token(request):
    """
    Alternative endpoint: If user is logged in via session (from allauth),
    return JWT tokens as JSON. Frontend can poll this after redirect.
    """
    try:
        if request.user.is_authenticated:
            user = request.user
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email if user.email else ''
            })
        else:
            return Response({'error': 'User not authenticated'}, status=401)
    
    except Exception as e:
        print(f"❌ Google OAuth token error: {str(e)}")
        return Response({'error': str(e)}, status=400)
