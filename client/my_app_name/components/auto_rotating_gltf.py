import reflex as rx
from typing import List

class AutoRotatingGLTF(rx.Component):
    """GLTF model that rotates slowly and is non-interactable."""
    tag = "AutoRotatingGLTFComponent"

    url: rx.Var[str] = ""
    position: rx.Var[List[float]] = [0, 0, 0]
    scale: rx.Var[float] = 1.0
    rotation_speed: rx.Var[float] = 0.5

    def add_custom_code(self) -> List[str]:
        return [
            """
            function AutoRotatingGLTFComponent({ url, position=[0,0,0], scale=1, rotationSpeed=0.5 }) {
                const [model, setModel] = React.useState(null);
                const groupRef = React.useRef();

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

                // Slow auto-rotation
                useFrame((state, delta) => {
                    if (groupRef.current) {
                        groupRef.current.rotation.y += rotationSpeed * delta;
                    }
                });

                if (!model) {
                    return (
                        <mesh position={position}>
                            <boxGeometry args={[1, 1, 1]} />
                            <meshStandardMaterial wireframe color="gray" />
                        </mesh>
                    );
                }

                return (
                    <group ref={groupRef} position={position} scale={scale}>
                        <primitive object={model} dispose={null} />
                    </group>
                );
            }
            """
        ]

