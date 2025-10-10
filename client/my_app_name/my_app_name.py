from my_app_name.draggable_gltf import DraggableGLTF
from my_app_name.static_gltf import GLTF
from reflex.components.component import NoSSRComponent
import reflex as rx
from .sphere import Sphere, create_sphere
from .cube import Cube, create_cube
from .dragcube import DraggableCube

class R3FCanvas(NoSSRComponent):
    library = "@react-three/fiber@9.0.0"
    tag = "Canvas"

    def add_custom_code(self) -> list[str]:
        return [
            """
            import React, { useRef } from 'react';
            import { useThree, useFrame } from '@react-three/fiber';
            import { useGLTF } from '@react-three/drei';
            """
        ]


class ThreeScene(rx.Component):
    tag = "ThreeScene"

    def add_custom_code(self) -> list[str]:
        return [
            """
            import * as THREE from 'three';
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



def index() -> rx.Component:
    """Main page with a rotating cube inside R3F Canvas."""
    return rx.box(
        R3FCanvas.create(
            ThreeScene.create(),
            #Sphere.create(position=[-2, 0, 1], color="#ffe66d", size=0.6),
            # create_sphere(position=[-2, 0, 1], color="#ff6b6b", size=0.6),
            Cube.create(position=[2, 0, 1], color="#4ecdc4", size=1.0),
            DraggableCube.create(position=[0, 0, 0], color="#ff6b6b", size=1.0),
            DraggableGLTF.create(
                url="cakeRoll/scene.gltf",
                position=[-2, 0, 1],
                scale=10,
                rotation=[0, 0, 0]
            ),
            GLTF.create(
                url="bunny/scene.gltf",
                position=[-3, 0, 1],
                scale=0.5,
                rotation=[0, 0, 0]
            ),
            style={  
                "width": "100%", 
                "height": "100vh"
            },
        ),
        style={
            "width": "100vw",
            "height": "100vh",
            "margin": "0",
            "padding": "0"
        }
    )

app = rx.App()
app.add_page(index)

if __name__ == "__main__":
    app.run()