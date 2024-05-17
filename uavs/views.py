from rest_framework import viewsets
from .models import UAV
from .serializers import UAVSerializer


class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer
