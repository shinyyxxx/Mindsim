from django.contrib import admin
from django.urls import path
import app_auth.views as auth_views
import app_notes.views as notes_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth endpoints
    path('register/', auth_views.register),
    path('login/', auth_views.login_view),
    path('logout/', auth_views.logout_view),
    path('is_logged_in/', auth_views.is_logged_in),
    # Notes endpoints
    path('notes/', notes_views.list_notes),
    path('notes/create/', notes_views.create_note),
    path('notes/<int:note_id>/', notes_views.get_note),
    path('notes/<int:note_id>/update/', notes_views.update_note),
    path('notes/<int:note_id>/delete/', notes_views.delete_note),
]

