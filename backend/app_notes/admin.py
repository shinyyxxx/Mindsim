from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_archived')
    list_filter = ('is_archived', 'created_at')
    search_fields = ('title', 'content', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
