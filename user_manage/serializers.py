from rest_framework import serializers
from django.contrib.auth import authenticate,login,logout
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password', 'password2', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove non-model field
        return User.objects.create_user(**validated_data)
            
# class UserRegistrationSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150, required=True)
#     email = serializers.EmailField(max_length=254, required=True)
#     first_name = serializers.CharField(max_length=30, required=True)
#     last_name = serializers.CharField(max_length=30, required=True)
#     phone_number = serializers.CharField(max_length=14, required=True)
#     password = serializers.CharField(write_only=True, required=True)
#     password2 = serializers.CharField(write_only=True, required=True)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'password2']

#     def validate(self, attrs): #password same chaki chaina bhanera checking
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError("Passwords do not match.")
#         return attrs
#     def validate_phone_number(self, value):
#         if User.objects.filter(phone_number=value).exists(): #checking whether the number already exists
#             raise serializers.ValidationError('Someone already used this number for registration.Plz try another number')
#         return value
    
#     def create(self, validated_data):
#         if User.objects.filter(username = validated_data['username']).exists(): #error msg for username #cant use def method because its already tagged as a unique = true in model ,it will cause IntegrityError
#             raise serializers.ValidationError('Username is already taken.')
#         user = User.objects.create_user(
#             username=validated_data['username'],

#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             phone_number=validated_data['phone_number']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name','phone_number')
