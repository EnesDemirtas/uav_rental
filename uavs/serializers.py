from rest_framework import serializers
from .models import UAV


class UAVSerializer(serializers.ModelSerializer):
    class Meta:
        model = UAV
        fields = '__all__'
