import os
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Fallback frontend URL if not set in environment
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:9090')

@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(View):
    @swagger_auto_schema(
        operation_description="Custom login endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['email', 'password'],
        ),
        responses={
            200: openapi.Response(description='Logged in successfully'),
            400: openapi.Response(description='Invalid credentials or email not verified'),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            try:
                user = User.objects.get(email=email)  # Find user by email
                email_address = EmailAddress.objects.get(user=user, email=email)
                
                if not email_address.verified:  # Check if the email is verified
                    return JsonResponse({'detail': 'Email not verified'}, status=400)

                # Authenticate using the username (since user object is already retrieved)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'detail': 'Logged in successfully'})
                else:
                    return JsonResponse({'detail': 'Invalid credentials'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'detail': 'Invalid credentials'}, status=400)
            except EmailAddress.DoesNotExist:
                return JsonResponse({'detail': 'Email not verified'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON'}, status=400)
