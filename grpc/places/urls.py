from django.urls import path

from . import views


urlpatterns = [
    path("api/places/create", views.create_place, name="create_place"),
    path("api/places/nearby", views.nearby_places, name="nearby_places"),
]


