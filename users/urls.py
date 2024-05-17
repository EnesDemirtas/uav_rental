from django.urls import path, include
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

from .views import (CreateUserView, LoginView, ManageUserView, CustomUserAddressViewSet, change_password,
                    SendEmailConfirmationTokenAPIView, ConfirmEmailView)

addresses_router = DefaultRouter()
addresses_router.register(r'addresses', CustomUserAddressViewSet)

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('profile/', ManageUserView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('profile/', include(addresses_router.urls)),
    path('profile/password_change/', change_password, name='change_password'),
    path('profile/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('profile/send_email_confirmation/', SendEmailConfirmationTokenAPIView.as_view(),
         name="send_email_confirmation"),
    path('profile/confirm_email/', ConfirmEmailView.as_view(), name="confirm_email")
]