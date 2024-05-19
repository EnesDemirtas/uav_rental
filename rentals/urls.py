from django.urls import path, include
from rest_framework.routers import DefaultRouter

from uavs.views import get_rent_page
from .views import RentalRecordViewSet

router = DefaultRouter()
router.register(r'rentals', RentalRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rental/', get_rent_page, name='rent'),
]
