import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import User


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    # Try to get data from JSON body first, fallback to form-data
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email', '').lower()
            password = data.get('password')
        else:
            email = request.POST.get('email', '').lower()
            password = request.POST.get('password')
    except (json.JSONDecodeError, AttributeError):
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password')

    if not email or not password:
        return JsonResponse({'error': 'email and password required'}, status=400)

    if '@' not in email:
        return JsonResponse({'error': 'Invalid email format'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'User with this email already exists'}, status=400)

    try:
        with transaction.atomic():
            user = User.objects.create_user(email=email, password=password)
        
        response = JsonResponse({
            'message': 'User registered successfully',
            'email': user.email
        }, status=201)
        response.set_cookie(
            'email',
            user.email,
            max_age=60*60*24*30,  # 30 days
            httponly=True,
            secure=True
        )
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """
    Login endpoint that accepts email and password.
    """
    if hasattr(request, 'user') and request.user.is_authenticated:
        return JsonResponse({'error': 'Already logged in'}, status=403)

    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email', '').lower()
            password = data.get('password')
        else:
            email = request.POST.get('email', '').lower()
            password = request.POST.get('password')
    except (json.JSONDecodeError, AttributeError):
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password')

    if not email or not password:
        return JsonResponse({'error': 'email and password required'}, status=400)

    user = authenticate(request, username=email, password=password)

    if user is not None:
        auth_login(request, user)
        response = JsonResponse({
            'message': 'Login successful',
            'email': user.email,
            'is_admin': user.is_admin
        }, status=200)
        response.set_cookie(
            'email',
            user.email,
            max_age=60*60*24*30, 
            httponly=True,
            secure=True
        )
        return response
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """
    Logout endpoint that clears the user session.
    """
    if hasattr(request, 'user') and request.user.is_authenticated:
        email = request.user.email
        auth_logout(request)
        response = JsonResponse({
            'message': 'Logout successful',
            'email': email
        }, status=200)
        # Clear the email cookie
        response.delete_cookie('email')
        return response
    else:
        return JsonResponse({'error': 'Not logged in'}, status=400)


@require_http_methods(["GET"])
def is_logged_in(request):
    """
    Check if user is currently logged in.
    """
    if hasattr(request, 'user') and request.user.is_authenticated:
        return JsonResponse({
            'logged_in': True,
            'email': request.user.email,
            'is_admin': request.user.is_admin
        })
    
    return JsonResponse({'logged_in': False, 'email': None})

