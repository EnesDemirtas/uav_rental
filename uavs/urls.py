from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import UAVViewSet

router = DefaultRouter()
router.register(r'uavs', UAVViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('uavs/rented', views.get_rented_uavs, name='rented_uavs'),
]
