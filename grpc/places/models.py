from __future__ import annotations

from django.contrib.gis.db import models


class PlaceIndex(models.Model):
    oid = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    location = models.PointField(geography=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["oid"]),
            models.Index(fields=["name"]),
        ]


