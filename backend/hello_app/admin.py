from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Hello


@admin.register(Hello)
class HelloAdmin(OSMGeoAdmin):
    list_display = ("id", "message", "properties_key")

