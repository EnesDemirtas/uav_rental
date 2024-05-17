from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UAVViewSet

router = DefaultRouter()
router.register(r'uavs', UAVViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
