from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CustomLoginSerializer
from rest_framework import serializers

class CustomLoginView(APIView):
    # Explicitly set to allow any authentication
    authentication_classes = []
    permission_classes = []

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(
        operation_description="Custom login endpoint",
        request_body=CustomLoginSerializer,
        responses={
            200: openapi.Response(description='Logged in successfully', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )),
            400: openapi.Response(description='Invalid credentials', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ))
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            return Response(
                {'detail': 'Logged in successfully'}, 
                status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return Response(
                {'detail': str(e.detail[0]) if e.detail else 'Validation error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )