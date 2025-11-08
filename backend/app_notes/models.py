from django.db import models
from django.contrib.gis.db import models as gis_models
from app_auth.models import User

SRID_3D = 4979

class MentalSphereSpatialData(models.Model):
    position = gis_models.PointField(dim=3, srid=SRID_3D)
    rotation = gis_models.PointField(dim=3, srid=SRID_3D)
    scale = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MindSpatialData(models.Model):
    position = gis_models.PointField(dim=3, srid=SRID_3D)
    rotation = gis_models.PointField(dim=3, srid=SRID_3D)
    scale = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MentalSphere(models.Model):
    name = models.CharField(max_length=200)
    detail = models.TextField(blank=True, default='')
    texture = models.CharField(max_length=255, blank=True, default='')
    color = models.CharField(max_length=7, default='#FFFFFF')
    rec_status = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mental_spheres')
    position_id = models.IntegerField(null=True, blank=True)
    rotation_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

class Mind(models.Model):
    name = models.CharField(max_length=200)
    detail = models.TextField(blank=True, default='')
    mental_spheres = models.JSONField(default=list)
    position = models.JSONField(default=list)
    rec_status = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='minds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
