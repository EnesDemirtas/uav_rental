from uuid import uuid4

from django.db import models


class UAV(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    weight = models.FloatField()
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def __str__(self):
    return self.brand + " " + self.model
