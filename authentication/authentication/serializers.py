# authentication/serializers.py

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

        # Check if the user exists
        try:
            user = User.objects.get(email=email)
            
            # Ensure the email is verified
            if not EmailAddress.objects.filter(user=user, email=email, verified=True).exists():
                raise serializers.ValidationError("Email is not verified.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        
        # Authenticate the user using the email (no need for username here)
        user = authenticate(email=email, password=password)  # Use email directly
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        # Return the user object along with the validated data
        data['user'] = user
        return data
