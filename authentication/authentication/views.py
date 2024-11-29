# authentication/views.py

from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from .serializers import CustomLoginSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
        serializer = CustomLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return JsonResponse({'detail': 'Logged in successfully'})
        else:
            raise ValidationError(serializer.errors)
