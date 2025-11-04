from uuid import uuid4
from django.contrib.gis.db import models as gis_models


class Hello(gis_models.Model):
    
    id = gis_models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message = gis_models.CharField(max_length=200)

    location = gis_models.PointField(dim=3, srid=4326, help_text="3D point location")
    
    properties_key = gis_models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = "hello"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.message} ({self.id})"

