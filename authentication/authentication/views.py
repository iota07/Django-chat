from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from .serializers import CustomLoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
        # Parse request data
        serializer = CustomLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Log in the user using Django session authentication
            
            # Return a successful response
            return JsonResponse({'detail': 'Logged in successfully'}, status=200)
        
        # Return validation errors if the serializer is not valid
        return JsonResponse(serializer.errors, status=400)
