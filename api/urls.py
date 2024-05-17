from django.urls import path, include

urlpatterns = [
    path('', include('users.urls')),
    path('', include('uavs.urls')),
    path('', include('rentals.urls')),
]
