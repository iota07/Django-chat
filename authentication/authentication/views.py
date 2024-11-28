from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.account.views import ConfirmEmailView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
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
        



class CustomConfirmEmailView(ConfirmEmailView):
    """
    Custom view to handle email confirmation and return a JSON response
    """
    def get(self, request, *args, **kwargs):
        # Override the default confirmation process here (optional)
        # Perform email confirmation and return a response
        try:
            # Calling the parent class's method to perform the confirmation
            response = super().get(request, *args, **kwargs)
            
            # Return a JSON response on success
            return Response({
                'message': 'Email confirmed successfully.',
                'status': 'success',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # If something goes wrong, return an error message
            return Response({
                'message': f'Error confirming email: {str(e)}',
                'status': 'error',
            }, status=status.HTTP_400_BAD_REQUEST)