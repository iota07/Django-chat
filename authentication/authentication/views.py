import os
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.account.views import ConfirmEmailView
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

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        try:
            # Perform email confirmation
            self.object = self.get_object()
            
            # Use the environment variable or fallback URL
            frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:9090')
            
            # Redirect to frontend login or home page
            return HttpResponseRedirect(f"{frontend_url}/login?email_confirmed=true")
        
        except Exception as e:
            # Use the environment variable or fallback URL
            frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:9090')
            
            # Return a redirect with error
            return HttpResponseRedirect(f"{frontend_url}/login?email_error={str(e)}")