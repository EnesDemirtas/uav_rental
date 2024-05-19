from django.urls import path, include
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view

from api import views

schema_view = get_schema_view(
    title="UAV Rental API",
    url="http://localhost:8000/",
    renderer_classes=[JSONOpenAPIRenderer],
)

urlpatterns = [
    path('', include('users.urls')),
    path('', include('uavs.urls')),
    path('', include('rentals.urls')),
    path('schema.json', schema_view),

    # Get endpoints to load pages.
    path('register/form', views.register),
    path('login/form', views.login),
    path('home/', views.home),
]
