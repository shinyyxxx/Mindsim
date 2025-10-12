from django.contrib import admin

from .models import PlaceIndex


@admin.register(PlaceIndex)
class PlaceIndexAdmin(admin.ModelAdmin):
    list_display = ("oid", "name", "created_at")
    search_fields = ("oid", "name")


