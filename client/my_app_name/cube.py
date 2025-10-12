# cube.py
import reflex as rx

class Cube(rx.Component):
    """A 3D cube component for R3F."""

    tag = "Cube"

    position: rx.Var[list[float]]
    color: rx.Var[str]
    size: rx.Var[float]

    def add_custom_code(self) -> list[str]:
        return [
            """
            export const Cube = ({ position=[0,0,0], color="skyblue", size=1 }) => {
              const meshRef = React.useRef();

              // Rotate animation
              useFrame(() => {
                if (meshRef.current) {
                  meshRef.current.rotation.y += 0.01;
                  meshRef.current.rotation.x += 0.01;
                }
              });

              return (
                <mesh ref={meshRef} position={position} castShadow receiveShadow>
                  <boxGeometry args={[size, size, size]} />
                  <meshStandardMaterial
                    color={color}
                    roughness={0.4}
                    metalness={0.3}
                  />
                </mesh>
              );
            };
            """
        ]


def create_cube(position=[0, 0, 0], color="skyblue", size=1.0) -> Cube:
    return Cube.create(position=position, color=color, size=size)
