from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            # Find user by email
            user = User.objects.get(email=email)
            
            # Check email verification
            if not EmailAddress.objects.filter(user=user, email=email, verified=True).exists():
                raise serializers.ValidationError("Email is not verified.")
            
            # Authenticate using username (Django's default auth uses username)
            authenticated_user = authenticate(username=user.username, password=password)
            
            if not authenticated_user:
                raise serializers.ValidationError("Invalid email or password.")
            
            data['user'] = authenticated_user
            return data
        
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")