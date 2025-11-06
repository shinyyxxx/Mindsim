from django.contrib import admin
from .models import MentalSphere, Mind, MentalSphereSpatialData


@admin.register(MentalSphereSpatialData)
class MentalSphereSpatialDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(MentalSphere)
class MentalSphereAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'color', 'rec_status', 'created_at')
    list_filter = ('rec_status', 'created_at', 'color')
    search_fields = ('name', 'detail', 'created_by__email')
    readonly_fields = ('created_at', 'updated_at', 'position_id', 'rotation_id')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('name', 'detail', 'created_by')
        }),
        ('Visual Properties', {
            'fields': ('texture', 'color')
        }),
        ('Spatial Data', {
            'fields': ('position_id', 'rotation_id')
        }),
        ('Status', {
            'fields': ('rec_status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Mind)
class MindAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'rec_status', 'created_at')
    list_filter = ('rec_status', 'created_at')
    search_fields = ('name', 'detail', 'created_by__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('name', 'detail', 'created_by')
        }),
        ('Mental Spheres', {
            'fields': ('mental_spheres',)
        }),
        ('Position & Status', {
            'fields': ('position', 'rec_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
