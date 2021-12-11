""" Users serializers """

# Django
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils import timezone

# DRF
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

# Models
from Root.Users.models import User, Profile

# Serializer
from Root.Users.api.serializers.profiles import ProfileModelSerializer

# Utilities
import jwt
from datetime import timedelta


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile",
        )


class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.
    Handle the request login data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    # https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
    def validate(self, data):
        """Check credentials."""

        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials (╥﹏╥)")
        if not user.is_verified:
            raise serializers.ValidationError("Account is not active yet ¯\_(ツ)_/¯ ")
        self.context["user"] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""

        """ token, created = Token.objects.get_or_create(user=self.context['user']) """
        token = RefreshToken.for_user(user=self.context["user"])
        return self.context["user"], token
