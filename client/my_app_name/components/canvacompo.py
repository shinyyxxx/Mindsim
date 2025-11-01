from reflex.components.component import NoSSRComponent
from typing import Any, Dict, List
import reflex as rx

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
    
class ModelViewer3D(rx.Component):
    """Load and display a GLB model using GLTFLoader."""
    tag = "ModelViewer3DComponent"

    url: rx.Var[str] = ""
    position: rx.Var[List[float]] = [0, 0, 0]
    scale: rx.Var[float] = 1.0
    rotation: rx.Var[List[float]] = [0, 0, 0]

    def add_custom_code(self) -> List[str]:
        return [
            """
            function ModelViewer3DComponent({ url, position=[0,0,0], scale=1, rotation=[0,0,0] }) {
                const [model, setModel] = React.useState(null);
                const modelRef = React.useRef();

                React.useEffect(() => {
                    if (!url) return;
                    let cancelled = false;

                    (async () => {
                        const mod = await import('three/examples/jsm/loaders/GLTFLoader.js');
                        const { GLTFLoader } = mod;
                        const loader = new GLTFLoader();

                        loader.load(
                            url,
                            (gltf) => {
                                if (!cancelled) {
                                    setModel(gltf.scene);
                                }
                            },
                            undefined,
                            (err) => console.error("Error loading model:", err)
                        );
                    })();

                    return () => { cancelled = true; };
                }, [url]);

                if (!model) {
                    return (
                        <mesh position={position}>
                            <boxGeometry args={[1, 1, 1]} />
                            <meshStandardMaterial wireframe color="gray" />
                        </mesh>
                    );
                }

                return (
                    <primitive
                        ref={modelRef}
                        object={model}
                        position={position}
                        scale={scale}
                        rotation={rotation}
                        dispose={null}
                    />
                );
            }
            """
        ]