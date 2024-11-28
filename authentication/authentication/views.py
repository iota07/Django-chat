from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'detail': 'Logged in successfully'})
                else:
                    return JsonResponse({'detail': 'Invalid credentials'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'detail': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Invalid JSON'}, status=400)