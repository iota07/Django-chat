import os
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress, EmailConfirmation
from django.core.exceptions import ObjectDoesNotExist
import json

# Fallback frontend URL if not set in environment
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:9090')

@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            try:
                user = User.objects.get(email=email)
                email_address = EmailAddress.objects.get(user=user, email=email)
                if not email_address.verified:
                    return JsonResponse({'detail': 'Email not verified'}, status=400)
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

class CustomEmailConfirmationView(View):
    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:9090')
        
        try:
            # Try to confirm the email
            email_confirmation = EmailConfirmation.objects.get(key=key)
            
            # Confirm the email
            email_confirmation.confirm()
            
            # Redirect to frontend with success
            return HttpResponseRedirect(f"{frontend_url}/login?email_confirmed=true")
        
        except ObjectDoesNotExist:
            # Invalid confirmation key
            return HttpResponseRedirect(f"{frontend_url}/login?email_error=invalid_key")
        
        except Exception as e:
            # Any other unexpected error
            return HttpResponseRedirect(f"{frontend_url}/login?email_error={str(e)}")