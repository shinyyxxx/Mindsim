from __future__ import annotations

import json
from typing import Any

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import PlaceIndex

from BTrees.OOBTree import OOBTree
import persistent


class Place(persistent.Persistent):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


def _bad_request(message: str, status: int = 400):
    return JsonResponse({"error": message}, status=status)


@csrf_exempt
def create_place(request):
    if request.method != "POST":
        return _bad_request("Method not allowed", 405)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _bad_request("Invalid JSON")

    name = payload.get("name")
    description = payload.get("description", "")
    lat = payload.get("lat")
    lng = payload.get("lng")

    if not name or lat is None or lng is None:
        return _bad_request("name, lat, lng are required")

    # Store in ZODB
    zroot = request.zodb_root
    if "places" not in zroot:
        zroot["places"] = OOBTree()

    place_obj = Place(name=name, description=description)
    # Generate an oid
    oid = f"p-{len(zroot['places']) + 1}"
    zroot["places"][oid] = place_obj

    # Index in PostGIS
    PlaceIndex.objects.create(
        oid=oid,
        name=name,
        location=Point(float(lng), float(lat)),
    )

    return JsonResponse({"oid": oid, "name": name})


def nearby_places(request):
    try:
        lat = float(request.GET.get("lat"))
        lng = float(request.GET.get("lng"))
        km = float(request.GET.get("km", 5))
    except Exception:
        return _bad_request("lat, lng must be numbers")

    ref = Point(lng, lat)
    qs = PlaceIndex.objects.filter(location__distance_lte=(ref, D(km=km))).distance(ref).order_by("distance")

    zroot = request.zodb_root
    places = zroot.get("places", OOBTree())
    results: list[dict[str, Any]] = []
    for idx in qs[:50]:
        po = places.get(idx.oid)
        results.append(
            {
                "oid": idx.oid,
                "name": idx.name,
                "lat": idx.location.y,
                "lng": idx.location.x,
                "description": getattr(po, "description", ""),
            }
        )

    return JsonResponse({"results": results})


