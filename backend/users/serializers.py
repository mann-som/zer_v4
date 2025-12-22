from attr import fields
from rest_framework import serializers
import serial
from wtforms import ValidationError
from .models import User
from . import utils

class UserRegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
            "mobile"
        )
        
    def create(self, validated_data):
        validated_data['user_code'] = utils.generate_user_code()
        return super().create(validated_data)

class UserDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "is_active",
            "is_staff",
            "is_kyc_verified",
            "is_email_verified", 
            "is_mobile_verified", 
            "delete_status",
            "created_at",
            "mobile", 
        )
        
class UpdateEmailSerializer(serializers.Serializer):
    user_code = serializers.CharField()
    email = serializers.EmailField()
    
    def validate(self, data):
        if not User.objects.filter(user_code=data['user_code'], delete_status=False).exists():
            raise serializers.ValidationError("Invalid user_code")
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already in use")
        
        return data
    
    def save(self):
        user = User.objects.get(user_code=self.validated_data['user_code'])
        
        # OTP verification later
        user.email = self.validated_data['email']
        user.save(update_fields=["email"])
        
        return user

class UpdateMobileSerializer(serializers.Serializer):
    user_code = serializers.CharField()
    mobile = serializers.CharField()
    
    def validate(self, data):
        if not User.objects.filter(user_code=data['user_code'], delete_status=False).exists():
            raise serializers.ValidationError("Invalid user_code")
        
        if User.objects.filter(mobile=data['mobile']).exists():
            raise serializers.ValidationError("Phone number already in use")
        
        return data
    
    def save(self):
        user = User.objects.get(user_code=self.validated_data['user_code'])
        
        # OTP verification later
        user.mobile = self.validated_data['mobile']
        user.save(update_fields=["mobile"])
        
        return user
    
class UpdateNameSerializer(serializers.Serializer):
    user_code = serializers.CharField()
    name = serializers.CharField()
    
    def validate(self, data):
        if not User.objects.filter(user_code=data['user_code'], delete_status=False).exists():
            raise serializers.ValidationError("Invalid user_code")
        
        # if User.objects.filter(email=data['email']).exists():
        #     raise serializers.ValidationError("Email already in use")
        
        return data
    
    def save(self):
        user = User.objects.get(user_code=self.validated_data['user_code'])
        
        # OTP verification later
        user.full_name = self.validated_data['name']
        user.save(update_fields=["full_name"])
        
        return user