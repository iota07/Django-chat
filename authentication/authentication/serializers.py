# authentication/serializers.py
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from allauth.account.models import EmailAddress

class CustomLoginSerializer(DefaultLoginSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        user = EmailAddress.objects.filter(email=email).first()

        if user and not user.verified:
            raise serializers.ValidationError("E-mail is not verified.")

        return super().validate(attrs)