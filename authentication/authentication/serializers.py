# authentication/serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check if the user exists and if email is verified
        try:
            user = User.objects.get(email=email)
            if not user.emailaddress_set.filter(email=email, verified=True).exists():
                raise serializers.ValidationError("Email is not verified.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        # Authenticate user
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        data['user'] = user
        return data
