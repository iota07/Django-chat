from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
import json

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
        



class CustomConfirmEmailView(View):
    def get(self, request, key, *args, **kwargs):
        try:
            confirmation = EmailConfirmationHMAC.from_key(key)
        except EmailConfirmation.DoesNotExist:
            return JsonResponse({'detail': 'Invalid confirmation key'}, status=400)

        confirmation.confirm(request)
        return JsonResponse({'detail': 'Email confirmed successfully'})