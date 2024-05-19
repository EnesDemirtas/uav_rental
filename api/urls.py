from django.urls import path, include

from api import views

urlpatterns = [
    path('', include('users.urls')),
    path('', include('uavs.urls')),
    path('', include('rentals.urls')),

    # Get endpoints to load pages.
    path('register/form', views.register),
    path('login/form', views.login),
    path('home/', views.home),
]
