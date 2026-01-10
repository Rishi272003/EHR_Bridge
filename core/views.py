from .models import EHRConnection
from rest_framework import mixins, status, viewsets
from .serializers import (
    EHRConnectionPostSerializer,
    UserLoginSerializer,
    EHRConnectionPatchSerializer,
    EHRConnectionSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from core import serializers
from rest_framework import status
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema


class EHRConnectionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = EHRConnection.objects.all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == "create":
            return EHRConnectionPostSerializer
        elif self.action in ["update", "partial_update"]:
            return EHRConnectionPatchSerializer
        return EHRConnectionSerializer


class AuthViewSet(viewsets.ViewSet):

    @extend_schema(request=UserLoginSerializer)
    @action(detail=False, methods=["post"], url_path="login",permission_classes=[AllowAny])
    def user_login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(
            request=request,
            username=email,   # works ONLY if USERNAME_FIELD = "email"
            password=password
        )

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "detail": "Login successful",
                "token": token.key,
                "created": created,
            },
            status=status.HTTP_200_OK,

        )
