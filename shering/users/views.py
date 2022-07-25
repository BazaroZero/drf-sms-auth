from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import users.schemas as schemas

from .models import User
from .serializers import RegistrationSerializer


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    @swagger_auto_schema(
        request_body=serializer_class, responses=schemas.user_post_response
    )
    def post(self, request):
        """Registration method. Takes phone, generates code and sends SMS"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=serializer_class, responses=schemas.user_put_response
    )
    def put(self, request):
        """Sign in method. Updates code for user and sends SMS again"""
        try:
            user: User = User.objects.get(phone=request.data["phone"])
        except User.DoesNotExist:
            raise ValidationError("User with this phone doesn't exist")
        if not user.is_code_expired(settings.CODE_RESEND_TIMEOUT):
            raise ValidationError(
                f"Can't send SMS earlier than {settings.CODE_RESEND_TIMEOUT} seconds after previous"
            )
        serializer = self.serializer_class(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    @swagger_auto_schema(responses=schemas.pair_response)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    @swagger_auto_schema(responses=schemas.refresh_response)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
