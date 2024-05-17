from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as BaseAuthTokenSerializer

from .models import CustomUser, CustomUserAddress


class CustomUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserAddress
        fields = ('id', 'user', 'street', 'city', 'state', 'zip_code')

    def create(self, validated_data):
        try:
            address = CustomUserAddress.objects.create(**validated_data)
            return address
        except ValueError as e:
            raise serializers.ValidationError({'error': str(e)})

    def update(self, instance, validated_data):
        """Update an address and return it"""
        address = super().update(instance, validated_data)
        return address


class CustomUserSerializer(serializers.ModelSerializer):
    addresses = CustomUserAddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'password', 'name', 'phone', 'is_staff', 'is_active', 'is_verified', 'created_at',
            'updated_at', 'addresses')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
            return user
        except ValueError as e:
            raise serializers.ValidationError({'error': str(e)})

    def update(self, instance, validated_data):
        """Update a user and return it"""
        user = super().update(instance, validated_data)
        return user


class AuthSerializer(serializers.Serializer):
    """serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user


class AuthTokenSerializer(BaseAuthTokenSerializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    username = None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)