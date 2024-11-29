from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from .serializers import CustomLoginSerializer

# Apply csrf_exempt to the view
@csrf_exempt
class CustomLoginView(APIView):
    @swagger_auto_schema(
        operation_description="Custom login endpoint",
        request_body=CustomLoginSerializer,
        responses={
            200: openapi.Response(description='Logged in successfully'),
            400: openapi.Response(description='Invalid credentials or email not verified'),
        },
    )
    def post(self, request, *args, **kwargs):
        # Deserialize the request data with the custom login serializer
        serializer = CustomLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return JsonResponse({'detail': 'Logged in successfully'})
        else:
            # If the serializer is not valid, raise validation error
            raise ValidationError(serializer.errors)
