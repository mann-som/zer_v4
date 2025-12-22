from tkinter.tix import Tree
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import serializers
from .models import User

@api_view(['POST'])
def register_user(request):
    serializer = serializers.UserRegistrationsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    return Response(
        {
            "user_code" : user.user_code,
            "email" : user.email,
            "message" : "User created successfully",
        },
        status=status.HTTP_201_CREATED
    )

class UserListView(APIView):
    ALLOWED_FILTERS = {"email", "mobile", "user_code"}
    def get(self, request):
        recievedParams = set(request.query_params.keys())
        invalidParams = recievedParams - self.ALLOWED_FILTERS
        
        if invalidParams:
            return Response(
                {
                    "error": f"Invalid query parameters: {', '.join(invalidParams)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        users = User.objects.filter(delete_status=False)

        # user_id = request.query_params.get("id")
        email = request.query_params.get("email")
        mobile = request.query_params.get("mobile")
        user_code = request.query_params.get("user_code")

        # if user_id:
        #     users = users.filter(id=user_id)
        if user_code:
            users = users.filter(user_code=user_code)

        if email:
            users = users.filter(email=email)

        if mobile:
            users = users.filter(mobile=mobile)

        serializer = serializers.UserDetailsSerializer(users, many=True)
        return Response(serializer.data)
                                   
@api_view(['POST'])
def update_mobile(request):
    serializer = serializers.UpdateMobileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    return Response(
        {
            "message": "Phone number updated successfully",
            "phone": user.mobile
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def update_name(request):
    serializer = serializers.UpdateNameSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    return Response(
        {
            "message": "Name updated successfully",
            "name": user.full_name
        },
        status=status.HTTP_200_OK
    )
             
@api_view(['POST'])
def update_email(request):
    serializer = serializers.UpdateEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    return Response(
        {
            "message": "Email updated successfully",
            "email": user.email
        },
        status=status.HTTP_200_OK
    )
    
@api_view(['POST'])
def delete_user(request):
    serializer = serializers.DeleteUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response(
        {
            "message": "User deleted successfully"
        },
        status=status.HTTP_200_OK
    )
    