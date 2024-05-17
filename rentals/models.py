from uuid import uuid4

from uavs.models import UAV
from users.models import CustomUser

from django.db import models


class RentalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    uav = models.ForeignKey(UAV, on_delete=models.DO_NOTHING)


def __str__(self):
    return self.user.name + " " + self.uav.brand + " " + self.uav.model
