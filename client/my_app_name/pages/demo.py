import reflex as rx
from ..components.draggable_gltf import DraggableGLTF
from ..components.base import base_page
from ..components.mentalfactor import MentalSphere, Mind
from ..components.room import Room, create_room, create_rooms
from ..components.player import Player, create_player
from ..components.collision import create_collision_boundaries
from ..components.canvacompo import R3FCanvas, ThreeScene, ModelViewer3D

def first_page() -> rx.Component:
    mental_factors = [
        {
            "name": "Focus",
            "detail": "Concentration and attention span\nAbility to maintain focus on tasks",
            "color": "#FF6B6B",
            "position": [2, 0, 0],
            "scale": 0.4,
        },
        {
            "name": "Creativity",
            "detail": "Innovative thinking\nAbility to generate new ideas",
            "color": "#4ECDC4",
            "position": [-2, 0, 0],
            "scale": 0.4,
        },
        {
            "name": "Mindfulness",
            "detail": "Present moment awareness\nEmotional regulation",
            "color": "#95E1D3",
            "position": [0, 2, 0],
            "scale": 0.4,
        },
        {
            "name": "Resilience",
            "detail": "Ability to recover from challenges\nEmotional strength",
            "color": "#F38181",
            "position": [0, -2, 0],
            "scale": 0.4,
        },
        {
            "name": "Clarity",
            "detail": "Mental clarity and organization\nCognitive processing",
            "color": "#AA96DA",
            "position": [0, 0, 2],
            "scale": 0.4,
        },
    ]

    room_configs = [
        {"position": (0,0,0), "width": 20, "length": 20, "height": 10, "color": "#FFFFFF", "doors": ["front"]},
        {"position": (0,0,16), "width": 8, "length": 12, "height": 10, "color": "#FFFFFF", "doors": ["back"]}
    ]
    my_child = R3FCanvas.create(
        ThreeScene.create(),
        create_rooms(room_configs),
        create_collision_boundaries(room_configs),
        create_player(),
        ModelViewer3D.create(
            url=rx.asset("girl.glb"),
            position=[0, 0, 0],
            scale=1.0,
        ),
        Mind.create(
            mental_spheres=mental_factors,
            container_radius=2.0,
            container_opacity=0.3,
            position=[0, 1.2, 0]
        ),
        style={
            "width": "100%",
            "height": "calc(100vh - 80px)",
        },
    )

    return base_page(my_child)