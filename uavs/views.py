from django.db import connection
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UAV
from .serializers import UAVSerializer


class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer


@api_view(['GET'])
def get_rent_page(request):
    return render(request, 'rent.html', context={
        'uav_id': str(request.query_params.get('uav_id', None))
    })


@api_view(['GET'])
def get_rented_uavs(request):
    with connection.cursor() as cursor:
        cursor.execute("select uu.id as uav_id, uu.brand as uav_brand, uu.model as uav_model, uu.weight as uav_weight, uu.category as uav_category " +
        "from rentals_rentalrecord rr " +
        "join uavs_uav uu " +
        "on rr.uav_id = uu.id " +
        "where NOW() between rr.start_datetime and rr.end_datetime;")

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return Response(data={'data': result}, status=200)

