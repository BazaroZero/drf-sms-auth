from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User
from .serializers import RegistrationSerializer

user_post_response_schema = {
    "400": openapi.Response(
        description="Error: Bad Request",
        examples={
            "application/json": {"phone": ["user with this phone already exists."]}
        },
    ),
}


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        request_body=serializer_class, responses=user_post_response_schema
    )
    def post(self, request):
        """Registration method. Takes phone, generates code and sends SMS"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request):
        """Authentication method. Updates code for user and sends SMS again"""
        try:
            user = User.objects.get(phone=request.data["phone"])
        except User.DoesNotExist:
            raise ValidationError("User with this phone doesn't exist")
        serializer = self.serializer_class(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


pair_response_schema = {
    "200": openapi.Response(
        description="",
        examples={
            "application/json": {
                "refresh": "header.payload.signature",
                "access": "header.payload.signature",
            }
        },
    ),
    "401": openapi.Response(
        description="Error: Unauthorized",
        examples={
            "application/json": {
                "detail": "No active account found with the given credentials",
            }
        },
    ),
}


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(responses=pair_response_schema)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


refresh_response_schema = {
    "200": openapi.Response(
        description="",
        examples={
            "application/json": {
                "access": "header.payload.signature",
                "refresh": "header.payload.signature",
            }
        },
    ),
    "401": openapi.Response(
        description="Error: Unauthorized",
        examples={
            "application/json": {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid",
            }
        },
    ),
}


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(responses=refresh_response_schema)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
