from django.contrib import admin
from django.urls import path
import app_auth.views as auth_views
import app_notes.views as mind_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth endpoints
    path('register/', auth_views.register),
    path('login/', auth_views.login_view),
    path('logout/', auth_views.logout_view),
    path('is_logged_in/', auth_views.is_logged_in),
    # Mental/Mind endpoints
    path('get_mind/', mind_views.get_mind),
    path('upsert_mind/', mind_views.upsert_mind),
    path('append_mental/', mind_views.add_mental_sphere),
    path('remove_mental/', mind_views.delete_mental_sphere),
    path('create_mental/', mind_views.create_sphere),
    path('get_all_mentals/', mind_views.list_spheres),
    path('get_mental/', mind_views.get_sphere),
    path('update_mental/', mind_views.update_sphere)
]

