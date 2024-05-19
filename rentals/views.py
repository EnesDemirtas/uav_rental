from rest_framework import viewsets

from .models import RentalRecord
from .serializers import RentalRecordSerializer


class RentalRecordViewSet(viewsets.ModelViewSet):
    queryset = RentalRecord.objects.all()
    serializer_class = RentalRecordSerializer
