# django imports
from datetime import timedelta

from django.contrib.auth import login, update_session_auth_hash
from django.utils import timezone
# knox imports
from knox.views import LoginView as KnoxLoginView
# rest_framework imports
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUserAddress, EmailConfirmationToken, CustomUser
# local app imports
from .serializers import CustomUserSerializer, AuthSerializer, AuthTokenSerializer, CustomUserAddressSerializer, \
    ChangePasswordSerializer
from .utils import send_confirmation_email


class CreateUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class LoginView(KnoxLoginView):
    # login view extending KnoxLoginView
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def perform_update(self, serializer):
        """Update authenticated user"""
        serializer.save(user=self.request.user)


class CustomUserAddressViewSet(viewsets.ModelViewSet):
    queryset = CustomUserAddress.objects.all()
    serializer_class = CustomUserAddressSerializer


class SendEmailConfirmationTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        token = EmailConfirmationToken.objects.create(user=user)
        send_confirmation_email(email=user.email, token_id=token.pk, user_id=user.pk)
        return Response(data=None, status=201)


class ConfirmEmailView(APIView):
    def get(self, request):
        token_id = request.GET.get('token_id', None)
        user_id = request.GET.get('user_id', None)
        try:
            token = EmailConfirmationToken.objects.get(pk=token_id)
            user = CustomUser.objects.get(pk=user_id)
            if token.user_id != user.pk:
                return Response(data={'error': 'Token is not valid'}, status=400)
            if token.created_at < timezone.now() - timedelta(minutes=5):
                return Response(data={'error': 'Token is expired'}, status=400)
            user.is_verified = True
            user.save()
            return Response(data={'message': 'Email is confirmed'}, status=200)
        except CustomUser.DoesNotExist:
            return Response(data={'error': 'User does not exist'}, status=400)
        except EmailConfirmationToken.DoesNotExist:
            return Response(data={'error': 'Token is not valid'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
