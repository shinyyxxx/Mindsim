from reflex.components.component import NoSSRComponent
import reflex as rx
from .draggable_gltf import DraggableGLTF
from .components.base import base_page
from .components.mentalfactor import MentalSphere, Mind
from .room import Room, create_room, create_rooms
from .player import Player, create_player
from .collision import create_collision_boundaries

class R3FCanvas(NoSSRComponent):
    library = "@react-three/fiber@9.0.0"
    tag = "Canvas"

    def add_custom_code(self) -> list[str]:
        return [
            """
            import React, { useRef, useState, useMemo } from 'react';
            import { useThree, useFrame } from '@react-three/fiber';
            import { useGLTF } from '@react-three/drei';
            import * as THREE from 'three';
            """
        ]

class ThreeScene(rx.Component):
    tag = "ThreeScene"

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const ThreeScene = () => {
              return (
                <>
                  {/* Global ambient light for base illumination */}
                  <ambientLight intensity={0.3} />

                  {/* Stronger spotlight with shadows */}
                  <spotLight
                    position={[10, 15, 10]}
                    angle={0.3}
                    penumbra={0.5}
                    intensity={1.2}
                    castShadow
                  />

                  {/* Directional light for nice shading */}
                  <directionalLight
                    position={[-5, 10, -5]}
                    intensity={0.8}
                    castShadow
                  />

                  {/* Ground plane to catch shadows */}
                  <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
                    <planeGeometry args={[50, 50]} />
                    <shadowMaterial opacity={0.3} />
                  </mesh>
                </>
              );
            };
            """
        ]


@rx.page(route="/")
def index() -> rx.Component:
    room_configs = [
        {"position": (0,0,0), "width": 20, "length": 20, "height": 10, "color": "#FFFFFF", "doors": ["right"]},
        {"position": (17.5,0,0), "width": 15, "length": 10, "height": 8, "color": "#FFFFFF", "doors": ["left"]}
    ]
    my_child = R3FCanvas.create(
        ThreeScene.create(),
        create_rooms(room_configs),
        create_collision_boundaries(room_configs),
        create_player(),
        DraggableGLTF.create(
            url="girl.glb",
            position=[0, -2.84, 3.5],
            scale=1
        ),
        DraggableGLTF.create(
            url="water.glb",
            position=[-1, 0.17, 4],
            scale=0.14,
            rotation=[0, 0, 0]
        ),
        style={
            "width": "100%",
            "height": "calc(100vh - 80px)"
        },
    )
    return base_page(my_child)

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
        Mind.create(
            mental_spheres=mental_factors,
            container_radius=3.0,
            container_opacity=0.3,
            position=[0, 1.2, 0]
        ),
        style={
            "width": "100%",
            "height": "calc(100vh - 80px)",
        },
    )

    return base_page(my_child)

def second_page() -> rx.Component:
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

    my_child = R3FCanvas.create(
        ThreeScene.create(),
        create_room(),
        create_player(),
        Mind.create(
            mental_spheres=mental_factors,
            container_radius=3.0,
            container_opacity=0.3,
            position=[0, 1.6, 0]
        ),
        style={
            "width": "100%",
            "height": "calc(100vh - 80px)",
        },
    )

    return base_page(my_child)


app = rx.App()
app.add_page(index)
app.add_page(first_page, route='/first')
app.add_page(second_page, route='/second')

if __name__ == "__main__":
    app.run()