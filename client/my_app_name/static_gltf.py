import reflex as rx

class GLTF(rx.Component):
    """Static GLTF model component for R3F."""

    tag = "GLTF"

    url: rx.Var[str]
    position: rx.Var[list[float]]
    scale: rx.Var[float]
    rotation: rx.Var[list[float]]
    animate_rotation: rx.Var[bool]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const GLTF = ({ 
              url, 
              position=[0,0,0], 
              scale=1, 
              rotation=[0,0,0],
              animate_rotation=false
            }) => {
              const groupRef = React.useRef();

              // Load GLTF model
              const { scene } = useGLTF(url);
              
              // Clone the scene to avoid reusing the same instance
              const clonedScene = React.useMemo(() => scene.clone(), [scene]);

              // Optional rotation animation
              useFrame(() => {
                if (animate_rotation && groupRef.current) {
                  groupRef.current.rotation.y += 0.01;
                }
              });

              return (
                <group
                  ref={groupRef}
                  position={position}
                  scale={scale}
                  rotation={rotation}
                  castShadow
                  receiveShadow
                >
                  <primitive object={clonedScene} castShadow receiveShadow />
                </group>
              );
            };
            """
        ]


def create_gltf(url, position=[0, 0, 0], scale=1.0, rotation=[0, 0, 0], animate_rotation=False) -> GLTF:
    """Helper function to create a static GLTF model."""
    return GLTF.create(
        url=url, 
        position=position, 
        scale=scale, 
        rotation=rotation,
        animate_rotation=animate_rotation
    )