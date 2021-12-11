""" Users view API """

# Django
from django.contrib.auth import get_user_model

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Serializers
from Root.Users.api.serializers.users import (
    UserModelSerializer,
    UserLoginSerializer
    # UserSignUpSerializer,
    # AccountVerificationSerializer,
)
from Root.Users.api.serializers.profiles import ProfileModelSerializer

# Permissions
# https://www.django-rest-framework.org/api-guide/permissions/
from rest_framework.permissions import AllowAny, IsAuthenticated
from Root.Users.api.permissions import IsAccountOwner

# Models
from Root.Users.models.users import User


class UserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    User view set.
    Handle sign up, login and account verification.
    """

    def get_permissions(self):
        """
        Assign permissions based on action.
        If the action is retrieve, custom permission is added
        so that only the same User can be edited and viewed
        """
        if self.action in ["signin", "signup", "verify"]:
            permissions = [AllowAny]
        elif self.action in [
            "profile",
            "retrieve",
            "update",
            "partial_update",
        ]:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=["POST"])
    def signin(self, request):
        """User sign in."""

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            "user": UserModelSerializer(user).data,
            # 'access_token': token
            "token": str(token.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)
