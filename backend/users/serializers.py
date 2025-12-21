from attr import fields
from rest_framework import serializers
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