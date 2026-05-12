from rest_framework import serializers
from .models import User,UserGender,UserType

class CustomerOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

class CustomerVerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

class SignUpSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)
    user_type = serializers.ChoiceField(choices=UserType.choices)
    gender = serializers.ChoiceField(choices=UserGender.choices, default=UserGender.OTHER)
    
    