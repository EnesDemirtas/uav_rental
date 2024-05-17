from rest_framework import serializers
from .models import RentalRecord


class RentalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalRecord
        fields = '__all__'
